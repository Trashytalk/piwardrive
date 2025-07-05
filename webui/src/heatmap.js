export function histogram(points, bins = 100, bounds = null) {
  const pts = points.map(([lat, lon]) => [Number(lat), Number(lon)]);
  let binsLat, binsLon;
  if (typeof bins === 'number') {
    binsLat = binsLon = bins;
  } else {
    [binsLat, binsLon] = bins;
  }
  let minLat, maxLat, minLon, maxLon;
  if (bounds) {
    [minLat, minLon, maxLat, maxLon] = bounds.map(Number);
  } else if (pts.length) {
    minLat = Math.min(...pts.map((p) => p[0]));
    maxLat = Math.max(...pts.map((p) => p[0]));
    minLon = Math.min(...pts.map((p) => p[1]));
    maxLon = Math.max(...pts.map((p) => p[1]));
  } else {
    return [
      Array.from({ length: binsLat }, () => Array(binsLon).fill(0)),
      [0, 0],
      [0, 0],
    ];
  }
  const hist = Array.from({ length: binsLat }, () => Array(binsLon).fill(0));
  if (maxLat === minLat || maxLon === minLon)
    return [hist, [minLat, maxLat], [minLon, maxLon]];
  for (const [lat, lon] of pts) {
    if (lat < minLat || lat > maxLat || lon < minLon || lon > maxLon) continue;
    let i = Math.floor(((lat - minLat) / (maxLat - minLat)) * binsLat);
    let j = Math.floor(((lon - minLon) / (maxLon - minLon)) * binsLon);
    if (i === binsLat) i -= 1;
    if (j === binsLon) j -= 1;
    hist[i][j] += 1;
  }
  return [hist, [minLat, maxLat], [minLon, maxLon]];
}

export function histogramPoints(hist, latRange, lonRange) {
  const [minLat, maxLat] = latRange.map(Number);
  const [minLon, maxLon] = lonRange.map(Number);
  const binsLat = hist.length;
  const binsLon = hist[0]?.length || 0;
  if (!binsLat || !binsLon) return [];
  const latStep = (maxLat - minLat) / binsLat;
  const lonStep = (maxLon - minLon) / binsLon;
  const pts = [];
  for (let i = 0; i < binsLat; i++) {
    for (let j = 0; j < binsLon; j++) {
      const c = hist[i][j];
      if (c <= 0) continue;
      const lat = minLat + (i + 0.5) * latStep;
      const lon = minLon + (j + 0.5) * lonStep;
      pts.push([lat, lon, c]);
    }
  }
  return pts;
}

export function densityMap(points, bins = 100, bounds = null, radius = 1) {
  const [hist, latRange, lonRange] = histogram(points, bins, bounds);
  const binsLat = hist.length;
  const binsLon = hist[0]?.length || 0;
  if (!binsLat || !binsLon) return [hist, latRange, lonRange];
  const dens = Array.from({ length: binsLon ? binsLat : 0 }, () =>
    Array(binsLon).fill(0)
  );
  for (let i = 0; i < binsLat; i++) {
    for (let j = 0; j < binsLon; j++) {
      const count = hist[i][j];
      if (count <= 0) continue;
      for (let di = -radius; di <= radius; di++) {
        for (let dj = -radius; dj <= radius; dj++) {
          const ii = i + di;
          const jj = j + dj;
          if (ii >= 0 && ii < binsLat && jj >= 0 && jj < binsLon)
            dens[ii][jj] += count;
        }
      }
    }
  }
  return [dens, latRange, lonRange];
}

export function coverageMap(points, bins = 100, bounds = null, radius = 1) {
  const [dens, latRange, lonRange] = densityMap(points, bins, bounds, radius);
  const cov = dens.map((row) => row.map((c) => (c > 0 ? 1 : 0)));
  return [cov, latRange, lonRange];
}
