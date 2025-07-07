"""
Advanced Visualization & Reporting Module for PiWardrive
Provides interactive 3D heatmaps,
    time-series analysis,
    clustering,
    and professional reporting
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from scipy.interpolate import griddata
from scipy.spatial.distance import cdist
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


@dataclass
class ScanPoint:
    """Data structure for wireless scan points"""

    latitude: float
    longitude: float
    elevation: float
    signal_strength: float
    timestamp: datetime
    ssid: str
    bssid: str
    channel: int
    encryption: str
    frequency: float
    vendor: str = ""
    device_type: str = ""


class Interactive3DHeatmap:
    """Interactive 3D heatmap visualization with elevation awareness"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.default_colorscale = self.config.get("colorscale", "Viridis")
        self.grid_resolution = self.config.get("grid_resolution", 50)
        self.elevation_factor = self.config.get("elevation_factor", 1.0)

    def create_3d_signal_heatmap(self, scan_data: List[ScanPoint]) -> go.Figure:
        """Create interactive 3D heatmap with elevation-aware signal strength"""
        try:
            df = self._prepare_dataframe(scan_data)

            # Create 3D scatter plot
            fig = go.Figure()

            # Add signal strength surface
            self._add_signal_surface(fig, df)

            # Add access point markers
            self._add_ap_markers(fig, df)

            # Add elevation contours
            self._add_elevation_contours(fig, df)

            # Configure layout
            self._configure_3d_layout(fig, "3D Signal Strength Heatmap")

            return fig

        except Exception as e:
            logger.error(f"Error creating 3D heatmap: {e}")
            raise

    def _prepare_dataframe(self, scan_data: List[ScanPoint]) -> pd.DataFrame:
        """Convert scan data to DataFrame"""
        _data = []
        for point in scan_data:
            data.append(
                {
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "elevation": point.elevation,
                    "signal": point.signal_strength,
                    "ssid": point.ssid,
                    "bssid": point.bssid,
                    "channel": point.channel,
                    "timestamp": point.timestamp,
                    "encryption": point.encryption,
                }
            )
        return pd.DataFrame(data)

    def _add_signal_surface(self, fig: go.Figure, df: pd.DataFrame):
        """Add interpolated signal strength surface"""
        # Create grid
        lat_range = np.linspace(df["lat"].min(), df["lat"].max(), self.grid_resolution)
        lon_range = np.linspace(df["lon"].min(), df["lon"].max(), self.grid_resolution)
        lat_grid, lon_grid = np.meshgrid(lat_range, lon_range)

        # Interpolate signal values
        points = df[["lat", "lon"]].values
        values = df["signal"].values

        signal_grid = griddata(
            points, values, (lat_grid, lon_grid), method="cubic", fill_value=np.nan
        )

        # Add surface
        fig.add_trace(
            go.Surface(
                x=lon_grid,
                y=lat_grid,
                z=signal_grid + df["elevation"].mean() * self.elevation_factor,
                colorscale=self.default_colorscale,
                name="Signal Strength",
                opacity=0.7,
                colorbar=dict(title="Signal Strength (dBm)", x=1.02),
            )
        )

    def _add_ap_markers(self, fig: go.Figure, df: pd.DataFrame):
        """Add access point markers"""
        unique_aps = (
            df.groupby("bssid")
            .agg(
                {
                    "lat": "mean",
                    "lon": "mean",
                    "elevation": "mean",
                    "signal": "max",
                    "ssid": "first",
                    "channel": "first",
                }
            )
            .reset_index()
        )

        fig.add_trace(
            go.Scatter3d(
                x=unique_aps["lon"],
                y=unique_aps["lat"],
                z=unique_aps["elevation"] * self.elevation_factor
                + unique_aps["signal"],
                mode="markers",
                marker=dict(
                    size=10,
                    color="red",
                    symbol="diamond",
                    line=dict(width=2, color="white"),
                ),
                name="Access Points",
                text=unique_aps["ssid"],
                customdata=unique_aps[["bssid", "channel"]],
                hovertemplate="<b>%{text}</b><br>"
                + "BSSID: %{customdata[0]}<br>"
                + "Channel: %{customdata[1]}<br>"
                + "Max Signal: %{z:.1f} dBm<extra></extra>",
            )
        )

    def _add_elevation_contours(self, fig: go.Figure, df: pd.DataFrame):
        """Add elevation contour lines"""
        if df["elevation"].std() > 0:  # Only if elevation varies
            lat_range = np.linspace(df["lat"].min(), df["lat"].max(), 30)
            lon_range = np.linspace(df["lon"].min(), df["lon"].max(), 30)
            lat_grid, lon_grid = np.meshgrid(lat_range, lon_range)

            # Interpolate elevation
            points = df[["lat", "lon"]].values
            elevations = df["elevation"].values

            elev_grid = griddata(
                points, elevations, (lat_grid, lon_grid), method="linear", fill_value=0
            )

            fig.add_trace(
                go.Surface(
                    x=lon_grid,
                    y=lat_grid,
                    z=elev_grid * self.elevation_factor,
                    colorscale="Greys",
                    opacity=0.2,
                    showscale=False,
                    name="Terrain",
                )
            )

    def _configure_3d_layout(self, fig: go.Figure, title: str):
        """Configure 3D plot layout"""
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title="Longitude",
                yaxis_title="Latitude",
                zaxis_title="Elevation + Signal (dBm)",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            ),
            width=1000,
            height=700,
            showlegend=True,
        )


class TimeSeriesAnalysis:
    """Time-series analysis with pattern recognition"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.window_size = self.config.get("window_size", 10)

    def create_timeline_analysis(self, scan_data: List[ScanPoint]) -> go.Figure:
        """Create comprehensive timeline analysis with pattern recognition"""
        try:
            df = pd.DataFrame(
                [
                    {
                        "timestamp": point.timestamp,
                        "signal": point.signal_strength,
                        "ssid": point.ssid,
                        "bssid": point.bssid,
                        "channel": point.channel,
                        "encryption": point.encryption,
                    }
                    for point in scan_data
                ]
            )

            # Sort by timestamp
            df = df.sort_values("timestamp")

            # Create subplots
            fig = make_subplots(
                rows=4,
                cols=1,
                subplot_titles=[
                    "Signal Strength Timeline",
                    "Network Discovery Rate",
                    "Channel Utilization",
                    "Security Analysis",
                ],
                vertical_spacing=0.08,
                shared_xaxes=True,
            )

            # Add signal strength analysis
            self._add_signal_timeline(fig, df, row=1)

            # Add network discovery rate
            self._add_discovery_rate(fig, df, row=2)

            # Add channel utilization
            self._add_channel_analysis(fig, df, row=3)

            # Add security analysis
            self._add_security_timeline(fig, df, row=4)

            # Configure layout
            fig.update_layout(
                title="Comprehensive Wireless Timeline Analysis",
                height=1000,
                showlegend=True,
                hovermode="x unified",
            )

            return fig

        except Exception as e:
            logger.error(f"Error creating timeline analysis: {e}")
            raise

    def _add_signal_timeline(self, fig: go.Figure, df: pd.DataFrame, row: int):
        """Add signal strength timeline with moving averages"""
        # Calculate moving averages for top SSIDs
        top_ssids = df["ssid"].value_counts().head(5).index

        for ssid in top_ssids:
            _ssiddata = df[df["ssid"] == ssid].copy()
            ssid_data["moving_avg"] = (
                ssid_data["signal"]
                .rolling(window=self.window_size, min_periods=1)
                .mean()
            )

            # Add raw signal data
            fig.add_trace(
                go.Scatter(
                    x=ssid_data["timestamp"],
                    y=ssid_data["signal"],
                    mode="markers",
                    name=f"{ssid} (raw)",
                    opacity=0.3,
                    showlegend=False,
                ),
                row=row,
                col=1,
            )

            # Add moving average
            fig.add_trace(
                go.Scatter(
                    x=ssid_data["timestamp"],
                    y=ssid_data["moving_avg"],
                    mode="lines",
                    name=ssid,
                    line=dict(width=2),
                ),
                row=row,
                col=1,
            )

    def _add_discovery_rate(self, fig: go.Figure, df: pd.DataFrame, row: int):
        """Add network discovery rate analysis"""
        # Resample to 1-minute intervals
        df_resampled = (
            df.set_index("timestamp")
            .resample("1T")
            .agg({"bssid": "nunique", "ssid": "nunique"})
            .reset_index()
        )

        fig.add_trace(
            go.Scatter(
                x=df_resampled["timestamp"],
                y=df_resampled["bssid"],
                mode="lines+markers",
                name="Unique BSSIDs",
                line=dict(color="blue", width=2),
            ),
            row=row,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=df_resampled["timestamp"],
                y=df_resampled["ssid"],
                mode="lines+markers",
                name="Unique SSIDs",
                line=dict(color="green", width=2),
            ),
            row=row,
            col=1,
        )

    def _add_channel_analysis(self, fig: go.Figure, df: pd.DataFrame, row: int):
        """Add channel utilization analysis"""
        # Channel usage over time
        channel_data = (
            df.groupby(["timestamp", "channel"]).size().reset_index(name="count")
        )

        for channel in sorted(channel_data["channel"].unique()):
            ch_data = channel_data[channel_data["channel"] == channel]
            fig.add_trace(
                go.Scatter(
                    x=ch_data["timestamp"],
                    y=ch_data["count"],
                    mode="lines",
                    name=f"Ch {channel}",
                    line=dict(width=1),
                    showlegend=False,
                ),
                row=row,
                col=1,
            )

    def _add_security_timeline(self, fig: go.Figure, df: pd.DataFrame, row: int):
        """Add security analysis timeline"""
        # Security type distribution over time
        security_data = (
            df.groupby(["timestamp", "encryption"]).size().reset_index(name="count")
        )

        security_colors = {
            "Open": "red",
            "WEP": "orange",
            "WPA": "yellow",
            "WPA2": "lightgreen",
            "WPA3": "green",
        }

        for enc_type in security_data["encryption"].unique():
            enc_data = security_data[security_data["encryption"] == enc_type]
            fig.add_trace(
                go.Scatter(
                    x=enc_data["timestamp"],
                    y=enc_data["count"],
                    mode="lines",
                    name=enc_type,
                    line=dict(color=security_colors.get(enc_type, "gray"), width=2),
                    stackgroup="security",
                ),
                row=row,
                col=1,
            )


class GeospatialClustering:
    """Automatic grouping of related access points using spatial clustering"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.eps = self.config.get("eps", 0.001)  # ~100m at equator
        self.min_samples = self.config.get("min_samples", 3)

    def perform_clustering(self, scan_data: List[ScanPoint]) -> Dict[str, Any]:
        """Perform geospatial clustering of access points"""
        try:
            df = pd.DataFrame(
                [
                    {
                        "lat": point.latitude,
                        "lon": point.longitude,
                        "signal": point.signal_strength,
                        "ssid": point.ssid,
                        "bssid": point.bssid,
                        "channel": point.channel,
                        "encryption": point.encryption,
                    }
                    for point in scan_data
                ]
            )

            # Perform DBSCAN clustering
            coords = df[["lat", "lon"]].values
            clustering = DBSCAN(eps=self.eps, min_samples=self.min_samples)
            cluster_labels = clustering.fit_predict(coords)

            df["cluster"] = cluster_labels

            # Generate cluster statistics
            cluster_stats = self._generate_cluster_stats(df)

            # Create visualization
            fig = self._create_cluster_visualization(df)

            # Generate cluster analysis
            _analysis = self._analyze_clusters(df, cluster_stats)

            return {
                "clustered_data": df,
                "statistics": cluster_stats,
                "visualization": fig,
                "analysis": analysis,
            }

        except Exception as e:
            logger.error(f"Error performing clustering: {e}")
            raise

    def _generate_cluster_stats(self, df: pd.DataFrame) -> List[Dict]:
        """Generate statistics for each cluster"""
        __stats = []

        for cluster_id in df["cluster"].unique():
            if cluster_id == -1:  # Skip noise points
                continue

            cluster_data = df[df["cluster"] == cluster_id]

            stat = {
                "cluster_id": int(cluster_id),
                "ap_count": len(cluster_data),
                "unique_ssids": cluster_data["ssid"].nunique(),
                "unique_bssids": cluster_data["bssid"].nunique(),
                "avg_signal": float(cluster_data["signal"].mean()),
                "max_signal": float(cluster_data["signal"].max()),
                "min_signal": float(cluster_data["signal"].min()),
                "center_lat": float(cluster_data["lat"].mean()),
                "center_lon": float(cluster_data["lon"].mean()),
                "radius_km": self._calculate_cluster_radius(cluster_data),
                "channels": list(cluster_data["channel"].unique()),
                "encryption_types": list(cluster_data["encryption"].unique()),
                "dominant_ssid": (
                    cluster_data["ssid"].mode().iloc[0]
                    if len(cluster_data["ssid"].mode()) > 0
                    else "Unknown"
                ),
            }
            stats.append(stat)

        return sorted(stats, key=lambda x: x["ap_count"], reverse=True)

    def _calculate_cluster_radius(self, cluster_data: pd.DataFrame) -> float:
        """Calculate cluster radius in kilometers"""
        from geopy.distance import geodesic

        center_lat = cluster_data["lat"].mean()
        center_lon = cluster_data["lon"].mean()

        max_distance = 0
        for _, row in cluster_data.iterrows():
            distance = geodesic(
                (center_lat, center_lon), (row["lat"], row["lon"])
            ).kilometers
            max_distance = max(max_distance, distance)

        return round(max_distance, 3)

    def _create_cluster_visualization(self, df: pd.DataFrame) -> go.Figure:
        """Create cluster visualization"""
        fig = px.scatter_mapbox(
            df[df["cluster"] != -1],  # Exclude noise points
            lat="lat",
            lon="lon",
            color="cluster",
            size="signal",
            hover_name="ssid",
            hover_data=["bssid", "signal", "channel"],
            mapbox_style="open-street-map",
            zoom=10,
            title="Geospatial Access Point Clustering",
        )

        # Add cluster centers
        cluster_centers = (
            df[df["cluster"] != -1]
            .groupby("cluster")
            .agg({"lat": "mean", "lon": "mean"})
            .reset_index()
        )

        fig.add_trace(
            go.Scattermapbox(
                lat=cluster_centers["lat"],
                lon=cluster_centers["lon"],
                mode="markers",
                marker=dict(size=15, color="red", symbol="star"),
                name="Cluster Centers",
                text=[f"Cluster {cid}" for cid in cluster_centers["cluster"]],
                hovertemplate="<b>%{text}</b><br>Lat: %{lat}<br>Lon: %{lon}<extra></extra>",
            )
        )

        return fig

    def _analyze_clusters(self, df: pd.DataFrame, stats: List[Dict]) -> Dict[str, Any]:
        """Analyze clustering results"""
        _total_aps = len(df)
        clustered_aps = len(df[df["cluster"] != -1])
        noise_aps = len(df[df["cluster"] == -1])

        _analysis = {
            "total_access_points": total_aps,
            "clustered_access_points": clustered_aps,
            "noise_points": noise_aps,
            "clustering_efficiency": round(clustered_aps / total_aps * 100, 2),
            "num_clusters": len(stats),
            "avg_cluster_size": (
                round(np.mean([s["ap_count"] for s in stats]), 2) if stats else 0
            ),
            "largest_cluster": (
                max(stats, key=lambda x: x["ap_count"]) if stats else None
            ),
            "densest_cluster": (
                max(stats, key=lambda x: x["ap_count"] / (x["radius_km"] + 0.001))
                if stats
                else None
            ),
        }

        return analysis


class ProfessionalReporting:
    """Professional PDF report generation with charts and recommendations"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(
            ParagraphStyle(
                name="CustomTitle",
                parent=self.styles["Title"],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.darkblue,
            )
        )

        self.styles.add(
            ParagraphStyle(
                name="SectionHeader",
                parent=self.styles["Heading1"],
                fontSize=16,
                spaceAfter=12,
                textColor=colors.darkgreen,
                borderWidth=1,
                borderColor=colors.green,
                borderPadding=5,
            )
        )

    def generate_comprehensive_report(
        self,
        scan_data: List[ScanPoint],
        cluster_results: Dict = None,
        analysis_results: Dict = None,
    ) -> bytes:
        """Generate comprehensive PDF report"""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
            )

            story = []

            # Title page
            self._add_title_page(story, scan_data)

            # Executive summary
            self._add_executive_summary(story, scan_data, analysis_results)

            # Technical analysis
            self._add_technical_analysis(story, scan_data)

            # Security analysis
            self._add_security_analysis(story, scan_data)

            # Clustering analysis
            if cluster_results:
                self._add_clustering_analysis(story, cluster_results)

            # Recommendations
            self._add_recommendations(story, scan_data)

            # Appendix
            self._add_appendix(story, scan_data)

            doc.build(story)
            buffer.seek(0)
            return buffer.read()

        except Exception as e:
            logger.error(f"Error generating report: {e}")
            raise

    def _add_title_page(self, story: List, scan_data: List[ScanPoint]):
        """Add title page to report"""
        story.append(Paragraph("PiWardrive", self.styles["CustomTitle"]))
        story.append(
            Paragraph("Wireless Security Assessment Report", self.styles["Title"])
        )
        story.append(Spacer(1, 50))

        # Scan summary
        scan_info = [
            ["Scan Date:", scan_data[0].timestamp.strftime("%Y-%m-%d %H:%M:%S")],
            ["Total Scan Points:", str(len(scan_data))],
            [
                "Unique Access Points:",
                str(len(set(point.bssid for point in scan_data))),
            ],
            ["Duration:", str(scan_data[-1].timestamp - scan_data[0].timestamp)],
        ]

        info_table = Table(scan_info, colWidths=[2 * inch, 3 * inch])
        info_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 12),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(info_table)
        story.append(Spacer(1, 50))

    def _add_executive_summary(
        self, story: List, scan_data: List[ScanPoint], analysis_results: Dict = None
    ):
        """Add executive summary section"""
        story.append(Paragraph("Executive Summary", self.styles["SectionHeader"]))

        # Calculate key metrics
        _total_aps = len(set(point.bssid for point in scan_data))
        _open_networks = sum(1 for point in scan_data if point.encryption == "Open")
        _avg_signal = np.mean([point.signal_strength for point in scan_data])

        summary_text = """
        This report presents the results of a comprehensive wireless security assessment
        conducted using PiWardrive. The scan identified {total_aps} unique access points
        across {len(scan_data)} measurement points.

        Key findings include {open_networks} open networks requiring immediate attention,

        with an average signal strength of {avg_signal:.1f} dBm across all detected networks.

        The analysis reveals important security implications and provides actionable
        recommendations for improving the wireless security posture of the surveyed area.
        """

        story.append(Paragraph(summary_text, self.styles["Normal"]))
        story.append(Spacer(1, 20))

    def _add_technical_analysis(self, story: List, scan_data: List[ScanPoint]):
        """Add technical analysis section"""
        story.append(Paragraph("Technical Analysis", self.styles["SectionHeader"]))

        # Create statistics table
        df = pd.DataFrame(
            [
                {
                    "signal": point.signal_strength,
                    "channel": point.channel,
                    "encryption": point.encryption,
                }
                for point in scan_data
            ]
        )

        stats_data = [
            ["Metric", "Value"],
            ["Total Measurements", str(len(scan_data))],
            ["Unique Access Points", str(df["signal"].count())],
            ["Average Signal Strength", f"{df['signal'].mean():.1f} dBm"],
            [
                "Signal Range",
                f"{df['signal'].min():.1f} to {df['signal'].max():.1f} dBm",
            ],
            ["Most Common Channel", str(df["channel"].mode().iloc[0])],
            ["Channel Spread", f"{df['channel'].min()} - {df['channel'].max()}"],
        ]

        stats_table = Table(stats_data, colWidths=[3 * inch, 2 * inch])
        stats_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(stats_table)
        story.append(Spacer(1, 20))

    def _add_security_analysis(self, story: List, scan_data: List[ScanPoint]):
        """Add security analysis section"""
        story.append(Paragraph("Security Analysis", self.styles["SectionHeader"]))

        # Analyze encryption types
        encryption_counts = {}
        for point in scan_data:
            enc = point.encryption
            encryption_counts[enc] = encryption_counts.get(enc, 0) + 1

        security_text = """
        Security analysis reveals the following encryption distribution:

        """

        for enc_type, count in encryption_counts.items():
            percentage = (count / len(scan_data)) * 100
            security_text += f"• {enc_type}: {count} networks ({percentage:.1f}%)\n"

        story.append(Paragraph(security_text, self.styles["Normal"]))
        story.append(Spacer(1, 20))

    def _add_clustering_analysis(self, story: List, cluster_results: Dict):
        """Add clustering analysis section"""
        story.append(
            Paragraph("Geospatial Clustering Analysis", self.styles["SectionHeader"])
        )

        _analysis = cluster_results.get("analysis", {})
        __stats = cluster_results.get("statistics", [])

        clustering_text = """
        Geospatial clustering analysis identified {analysis.get('num_clusters',
            0)} distinct
        access point clusters with {analysis.get('clustering_efficiency',
            0):.1f}% efficiency.

        The largest cluster contains {analysis.get('largest_cluster',
            {}).get('ap_count',
            0)}
        access points, suggesting potential enterprise or campus deployments.
        """

        story.append(Paragraph(clustering_text, self.styles["Normal"]))
        story.append(Spacer(1, 20))

    def _add_recommendations(self, story: List, scan_data: List[ScanPoint]):
        """Add recommendations section"""
        story.append(Paragraph("Recommendations", self.styles["SectionHeader"]))

        # Generate recommendations based on findings
        open_count = sum(1 for point in scan_data if point.encryption == "Open")
        wep_count = sum(1 for point in scan_data if point.encryption == "WEP")

        recommendations = []

        if open_count > 0:
            recommendations.append(
                f"Secure {open_count} open networks with appropriate encryption"
            )

        if wep_count > 0:
            recommendations.append(
                f"Upgrade {wep_count} WEP-encrypted networks to WPA2/WPA3"
            )

        recommendations.extend(
            [
                "Implement regular wireless security audits",
                "Monitor for rogue access points",
                "Establish wireless security policies",
                "Consider implementing enterprise-grade wireless solutions",
            ]
        )

        for i, rec in enumerate(recommendations, 1):
            story.append(Paragraph(f"{i}. {rec}", self.styles["Normal"]))

        story.append(Spacer(1, 20))

    def _add_appendix(self, story: List, scan_data: List[ScanPoint]):
        """Add appendix with detailed data"""
        story.append(
            Paragraph("Appendix: Detailed Scan Data", self.styles["SectionHeader"])
        )

        # Sample of scan data
        sample_data = scan_data[:20]  # First 20 points

        table_data = [["SSID", "BSSID", "Channel", "Signal", "Encryption"]]
        for point in sample_data:
            table_data.append(
                [
                    point.ssid[:20] if len(point.ssid) > 20 else point.ssid,
                    point.bssid,
                    str(point.channel),
                    f"{point.signal_strength:.1f}",
                    point.encryption,
                ]
            )

        detail_table = Table(
            table_data,
            colWidths=[1.5 * inch, 1.5 * inch, 0.8 * inch, 0.8 * inch, 1 * inch],
        )
        detail_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )

        story.append(detail_table)


class ComparativeAnalysis:
    """Before/after scanning comparisons and analysis"""

    def __init__(self, config: Dict = None):
        self.config = config or {}

    def compare_scans(
        self, before_data: List[ScanPoint], after_data: List[ScanPoint]
    ) -> Dict[str, Any]:
        """Compare two sets of scan data for changes"""
        try:
            # Convert to DataFrames
            before_df = self._prepare_comparison_df(before_data, "before")
            after_df = self._prepare_comparison_df(after_data, "after")

            # Analyze changes
            changes = self._analyze_changes(before_df, after_df)

            # Create visualizations
            fig = self._create_comparison_visualization(before_df, after_df, changes)

            # Generate change report
            report = self._generate_change_report(changes)

            return {
                "changes": changes,
                "visualization": fig,
                "report": report,
                "before_stats": self._calculate_stats(before_df),
                "after_stats": self._calculate_stats(after_df),
            }

        except Exception as e:
            logger.error(f"Error comparing scans: {e}")
            raise

    def _prepare_comparison_df(
        self, scan_data: List[ScanPoint], scan_type: str
    ) -> pd.DataFrame:
        """Prepare DataFrame for comparison"""
        _data = []
        for point in scan_data:
            data.append(
                {
                    "bssid": point.bssid,
                    "ssid": point.ssid,
                    "channel": point.channel,
                    "signal": point.signal_strength,
                    "encryption": point.encryption,
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "timestamp": point.timestamp,
                    "scan_type": scan_type,
                }
            )
        return pd.DataFrame(data)

    def _analyze_changes(
        self, before_df: pd.DataFrame, after_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """Analyze changes between scans"""
        before_bssids = set(before_df["bssid"].unique())
        after_bssids = set(after_df["bssid"].unique())

        # Identify changes
        new_aps = after_bssids - before_bssids
        disappeared_aps = before_bssids - after_bssids
        common_aps = before_bssids & after_bssids

        # Analyze signal changes for common APs
        signal_changes = []
        for bssid in common_aps:
            before_signal = before_df[before_df["bssid"] == bssid]["signal"].mean()
            after_signal = after_df[after_df["bssid"] == bssid]["signal"].mean()
            change = after_signal - before_signal

            if abs(change) > 5:  # Significant change threshold
                signal_changes.append(
                    {
                        "bssid": bssid,
                        "ssid": before_df[before_df["bssid"] == bssid]["ssid"].iloc[0],
                        "before_signal": before_signal,
                        "after_signal": after_signal,
                        "change": change,
                    }
                )

        # Analyze encryption changes
        encryption_changes = []
        for bssid in common_aps:
            before_enc = before_df[before_df["bssid"] == bssid]["encryption"].iloc[0]
            after_enc = after_df[after_df["bssid"] == bssid]["encryption"].iloc[0]

            if before_enc != after_enc:
                encryption_changes.append(
                    {
                        "bssid": bssid,
                        "ssid": before_df[before_df["bssid"] == bssid]["ssid"].iloc[0],
                        "before_encryption": before_enc,
                        "after_encryption": after_enc,
                    }
                )

        return {
            "new_aps": list(new_aps),
            "disappeared_aps": list(disappeared_aps),
            "common_aps": list(common_aps),
            "signal_changes": signal_changes,
            "encryption_changes": encryption_changes,
            "total_before": len(before_bssids),
            "total_after": len(after_bssids),
            "net_change": len(after_bssids) - len(before_bssids),
        }

    def _create_comparison_visualization(
        self, before_df: pd.DataFrame, after_df: pd.DataFrame, changes: Dict
    ) -> go.Figure:
        """Create comparison visualization"""
        # Create subplots
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=[
                "Access Point Count Comparison",
                "Signal Strength Distribution",
                "Channel Usage Comparison",
                "Security Changes",
            ],
            specs=[
                [{"type": "bar"}, {"type": "histogram"}],
                [{"type": "bar"}, {"type": "bar"}],
            ],
        )

        # AP count comparison
        fig.add_trace(
            go.Bar(
                x=["Before", "After"],
                y=[changes["total_before"], changes["total_after"]],
                name="Total APs",
                marker_color=["blue", "red"],
            ),
            row=1,
            col=1,
        )

        # Signal strength distributions
        fig.add_trace(
            go.Histogram(x=before_df["signal"], name="Before", opacity=0.7, nbinsx=30),
            row=1,
            col=2,
        )

        fig.add_trace(
            go.Histogram(x=after_df["signal"], name="After", opacity=0.7, nbinsx=30),
            row=1,
            col=2,
        )

        # Channel usage comparison
        before_channels = before_df["channel"].value_counts().sort_index()
        after_channels = after_df["channel"].value_counts().sort_index()

        all_channels = sorted(set(before_channels.index) | set(after_channels.index))

        fig.add_trace(
            go.Bar(
                x=all_channels,
                y=[before_channels.get(ch, 0) for ch in all_channels],
                name="Before Channels",
                opacity=0.7,
            ),
            row=2,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=all_channels,
                y=[after_channels.get(ch, 0) for ch in all_channels],
                name="After Channels",
                opacity=0.7,
            ),
            row=2,
            col=1,
        )

        # Security analysis
        security_data = [
            ["New APs", len(changes["new_aps"])],
            ["Disappeared APs", len(changes["disappeared_aps"])],
            ["Signal Changes", len(changes["signal_changes"])],
            ["Encryption Changes", len(changes["encryption_changes"])],
        ]

        fig.add_trace(
            go.Bar(
                x=[item[0] for item in security_data],
                y=[item[1] for item in security_data],
                name="Changes",
                marker_color=["green", "red", "orange", "purple"],
            ),
            row=2,
            col=2,
        )

        fig.update_layout(
            title="Before/After Scan Comparison", height=800, showlegend=True
        )

        return fig

    def _calculate_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate statistics for a scan"""
        return {
            "total_aps": df["bssid"].nunique(),
            "avg_signal": df["signal"].mean(),
            "signal_std": df["signal"].std(),
            "channels_used": df["channel"].nunique(),
            "encryption_distribution": df["encryption"].value_counts().to_dict(),
        }

    def _generate_change_report(self, changes: Dict) -> str:
        """Generate textual change report"""
        report = """
        SCAN COMPARISON REPORT
        ======================

        Network Changes:
        - New access points detected: {len(changes['new_aps'])}
        - Access points disappeared: {len(changes['disappeared_aps'])}
        - Net change: {changes['net_change']} access points

        Signal Strength Changes:
        - {len(changes['signal_changes'])} access points showed significant signal changes

        Security Changes:
        - {len(changes['encryption_changes'])} access points changed encryption

        """

        if changes["signal_changes"]:
            report += "\nSignificant Signal Changes:\n"
            for change in changes["signal_changes"][:5]:  # Top 5
                report += f"- {change['ssid']}: {change['change']:+.1f} dBm\n"

        if changes["encryption_changes"]:
            report += "\nEncryption Changes:\n"
            for change in changes["encryption_changes"]:
                report += f"- {change['ssid']}: {change['before_encryption']} → {change['after_encryption']}\n"

        return report
