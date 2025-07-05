"""
Real-time update performance optimization for PiWardrive.

This module provides optimized WebSocket and SSE handlers, efficient
data streaming, and client-side performance improvements.
"""

import asyncio
import gzip
import json
import logging
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Set, Callable
from weakref import WeakSet

import websockets
from fastapi import WebSocket, Request
from fastapi.responses import StreamingResponse
from starlette.websockets import WebSocketDisconnect

logger = logging.getLogger(__name__)


@dataclass
class ConnectionMetrics:
    """Metrics for WebSocket/SSE connection performance."""
    connection_id: str
    connection_type: str  # 'websocket' or 'sse'
    connected_at: float
    messages_sent: int
    bytes_sent: int
    last_activity: float
    errors: int
    
    @property
    def connection_duration(self) -> float:
        return time.time() - self.connected_at
    
    @property
    def messages_per_second(self) -> float:
        duration = self.connection_duration
        return self.messages_sent / duration if duration > 0 else 0
    
    @property
    def bytes_per_second(self) -> float:
        duration = self.connection_duration
        return self.bytes_sent / duration if duration > 0 else 0


class OptimizedWebSocketManager:
    """Optimized WebSocket connection manager with performance monitoring."""
    
    def __init__(self, max_connections: int = 1000, compression: bool = True):
        self.max_connections = max_connections
        self.compression = compression
        self.connections: Dict[str, WebSocket] = {}
        self.connection_groups: Dict[str, Set[str]] = defaultdict(set)
        self.connection_metrics: Dict[str, ConnectionMetrics] = {}
        self.message_buffer: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.stats = {
            "total_connections": 0,
            "active_connections": 0,
            "messages_sent": 0,
            "bytes_sent": 0,
            "errors": 0
        }
    
    async def connect(self, websocket: WebSocket, connection_id: str, group: Optional[str] = None) -> bool:
        """Connect a WebSocket with performance optimization."""
        if len(self.connections) >= self.max_connections:
            logger.warning(f"Max connections reached ({self.max_connections})")
            return False
        
        try:
            await websocket.accept()
            
            self.connections[connection_id] = websocket
            if group:
                self.connection_groups[group].add(connection_id)
            
            self.connection_metrics[connection_id] = ConnectionMetrics(
                connection_id=connection_id,
                connection_type="websocket",
                connected_at=time.time(),
                messages_sent=0,
                bytes_sent=0,
                last_activity=time.time(),
                errors=0
            )
            
            self.stats["total_connections"] += 1
            self.stats["active_connections"] = len(self.connections)
            
            logger.info(f"WebSocket connected: {connection_id} (group: {group})")
            return True
            
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False
    
    async def disconnect(self, connection_id: str, group: Optional[str] = None):
        """Disconnect a WebSocket and clean up resources."""
        if connection_id in self.connections:
            del self.connections[connection_id]
        
        if group and connection_id in self.connection_groups[group]:
            self.connection_groups[group].discard(connection_id)
        
        if connection_id in self.connection_metrics:
            del self.connection_metrics[connection_id]
        
        if connection_id in self.message_buffer:
            del self.message_buffer[connection_id]
        
        self.stats["active_connections"] = len(self.connections)
        
        logger.info(f"WebSocket disconnected: {connection_id}")
    
    async def send_message(self, connection_id: str, message: Dict[str, Any]) -> bool:
        """Send a message to a specific connection."""
        if connection_id not in self.connections:
            return False
        
        websocket = self.connections[connection_id]
        metrics = self.connection_metrics[connection_id]
        
        try:
            # Serialize message
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
            
            # Compress if enabled and message is large
            if self.compression and len(message_bytes) > 1024:
                compressed = gzip.compress(message_bytes)
                if len(compressed) < len(message_bytes):
                    await websocket.send_bytes(compressed)
                    message_bytes = compressed
                else:
                    await websocket.send_text(message_json)
            else:
                await websocket.send_text(message_json)
            
            # Update metrics
            metrics.messages_sent += 1
            metrics.bytes_sent += len(message_bytes)
            metrics.last_activity = time.time()
            
            self.stats["messages_sent"] += 1
            self.stats["bytes_sent"] += len(message_bytes)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send message to {connection_id}: {e}")
            metrics.errors += 1
            self.stats["errors"] += 1
            await self.disconnect(connection_id)
            return False
    
    async def broadcast_to_group(self, group: str, message: Dict[str, Any]) -> int:
        """Broadcast a message to all connections in a group."""
        if group not in self.connection_groups:
            return 0
        
        connection_ids = list(self.connection_groups[group])
        success_count = 0
        
        # Send to all connections concurrently
        tasks = []
        for connection_id in connection_ids:
            tasks.append(self.send_message(connection_id, message))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result is True:
                success_count += 1
        
        return success_count
    
    async def broadcast_to_all(self, message: Dict[str, Any]) -> int:
        """Broadcast a message to all connections."""
        connection_ids = list(self.connections.keys())
        success_count = 0
        
        tasks = []
        for connection_id in connection_ids:
            tasks.append(self.send_message(connection_id, message))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if result is True:
                success_count += 1
        
        return success_count
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics."""
        stats = dict(self.stats)
        stats["connection_metrics"] = {}
        
        for connection_id, metrics in self.connection_metrics.items():
            stats["connection_metrics"][connection_id] = {
                "connection_duration": metrics.connection_duration,
                "messages_sent": metrics.messages_sent,
                "bytes_sent": metrics.bytes_sent,
                "messages_per_second": metrics.messages_per_second,
                "bytes_per_second": metrics.bytes_per_second,
                "errors": metrics.errors
            }
        
        return stats
    
    async def cleanup_stale_connections(self, timeout: float = 300.0):
        """Clean up connections that haven't been active recently."""
        current_time = time.time()
        stale_connections = []
        
        for connection_id, metrics in self.connection_metrics.items():
            if current_time - metrics.last_activity > timeout:
                stale_connections.append(connection_id)
        
        for connection_id in stale_connections:
            logger.info(f"Cleaning up stale connection: {connection_id}")
            await self.disconnect(connection_id)
        
        return len(stale_connections)


class OptimizedSSEManager:
    """Optimized Server-Sent Events manager."""
    
    def __init__(self, max_connections: int = 1000):
        self.max_connections = max_connections
        self.active_streams: Dict[str, bool] = {}
        self.stream_metrics: Dict[str, ConnectionMetrics] = {}
        self.stats = {
            "total_streams": 0,
            "active_streams": 0,
            "events_sent": 0,
            "bytes_sent": 0
        }
    
    async def create_stream(self, stream_id: str, event_generator: Callable) -> StreamingResponse:
        """Create an optimized SSE stream."""
        if len(self.active_streams) >= self.max_connections:
            logger.warning(f"Max SSE streams reached ({self.max_connections})")
            return StreamingResponse(
                self._error_generator("Max connections reached"),
                media_type="text/event-stream"
            )
        
        self.active_streams[stream_id] = True
        self.stream_metrics[stream_id] = ConnectionMetrics(
            connection_id=stream_id,
            connection_type="sse",
            connected_at=time.time(),
            messages_sent=0,
            bytes_sent=0,
            last_activity=time.time(),
            errors=0
        )
        
        self.stats["total_streams"] += 1
        self.stats["active_streams"] = len(self.active_streams)
        
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
            "Content-Type": "text/event-stream"
        }
        
        return StreamingResponse(
            self._wrap_event_generator(stream_id, event_generator),
            media_type="text/event-stream",
            headers=headers
        )
    
    async def _wrap_event_generator(self, stream_id: str, event_generator: Callable):
        """Wrap event generator with performance monitoring."""
        try:
            async for event_data in event_generator():
                if stream_id not in self.active_streams:
                    break
                
                # Format SSE event
                if isinstance(event_data, dict):
                    event_json = json.dumps(event_data)
                else:
                    event_json = str(event_data)
                
                event_str = f"data: {event_json}\n\n"
                event_bytes = event_str.encode('utf-8')
                
                # Update metrics
                metrics = self.stream_metrics[stream_id]
                metrics.messages_sent += 1
                metrics.bytes_sent += len(event_bytes)
                metrics.last_activity = time.time()
                
                self.stats["events_sent"] += 1
                self.stats["bytes_sent"] += len(event_bytes)
                
                yield event_bytes
                
        except Exception as e:
            logger.error(f"SSE stream error for {stream_id}: {e}")
            metrics = self.stream_metrics.get(stream_id)
            if metrics:
                metrics.errors += 1
        finally:
            self._cleanup_stream(stream_id)
    
    async def _error_generator(self, error_message: str):
        """Generate error event for SSE."""
        error_event = f"event: error\ndata: {error_message}\n\n"
        yield error_event.encode('utf-8')
    
    def _cleanup_stream(self, stream_id: str):
        """Clean up stream resources."""
        if stream_id in self.active_streams:
            del self.active_streams[stream_id]
        
        if stream_id in self.stream_metrics:
            del self.stream_metrics[stream_id]
        
        self.stats["active_streams"] = len(self.active_streams)
        
        logger.info(f"SSE stream cleaned up: {stream_id}")
    
    def get_stream_stats(self) -> Dict[str, Any]:
        """Get SSE stream statistics."""
        stats = dict(self.stats)
        stats["stream_metrics"] = {}
        
        for stream_id, metrics in self.stream_metrics.items():
            stats["stream_metrics"][stream_id] = {
                "connection_duration": metrics.connection_duration,
                "messages_sent": metrics.messages_sent,
                "bytes_sent": metrics.bytes_sent,
                "messages_per_second": metrics.messages_per_second,
                "bytes_per_second": metrics.bytes_per_second,
                "errors": metrics.errors
            }
        
        return stats


class DataStreamOptimizer:
    """Optimizer for data streaming performance."""
    
    def __init__(self, compression_threshold: int = 1024):
        self.compression_threshold = compression_threshold
        self.serialization_cache: Dict[str, str] = {}
        self.cache_max_size = 1000
    
    def optimize_data_for_streaming(self, data: Any, cache_key: Optional[str] = None) -> Dict[str, Any]:
        """Optimize data for streaming by reducing size and improving serialization."""
        if cache_key and cache_key in self.serialization_cache:
            return json.loads(self.serialization_cache[cache_key])
        
        optimized = self._optimize_data_structure(data)
        
        if cache_key:
            # Cache serialized data
            if len(self.serialization_cache) >= self.cache_max_size:
                # Remove oldest entries
                oldest_keys = list(self.serialization_cache.keys())[:100]
                for key in oldest_keys:
                    del self.serialization_cache[key]
            
            self.serialization_cache[cache_key] = json.dumps(optimized)
        
        return optimized
    
    def _optimize_data_structure(self, data: Any) -> Any:
        """Optimize data structure for streaming."""
        if isinstance(data, dict):
            optimized = {}
            for key, value in data.items():
                # Remove null values to reduce size
                if value is not None:
                    optimized[key] = self._optimize_data_structure(value)
            return optimized
        
        elif isinstance(data, list):
            return [self._optimize_data_structure(item) for item in data if item is not None]
        
        elif isinstance(data, float):
            # Round floats to reduce precision and size
            return round(data, 6)
        
        elif isinstance(data, str):
            # Truncate very long strings
            if len(data) > 1000:
                return data[:997] + "..."
            return data
        
        return data
    
    def should_compress(self, data: str) -> bool:
        """Check if data should be compressed."""
        return len(data.encode('utf-8')) > self.compression_threshold
    
    def compress_data(self, data: str) -> bytes:
        """Compress data for transmission."""
        return gzip.compress(data.encode('utf-8'))


class RealTimeUpdateOptimizer:
    """Optimizer for real-time updates combining WebSocket and SSE."""
    
    def __init__(self):
        self.websocket_manager = OptimizedWebSocketManager()
        self.sse_manager = OptimizedSSEManager()
        self.data_optimizer = DataStreamOptimizer()
        self.update_throttle: Dict[str, float] = {}
        self.throttle_interval = 0.1  # 100ms minimum between updates
    
    async def send_real_time_update(self, update_type: str, data: Any, target_group: Optional[str] = None):
        """Send a real-time update through the best available channel."""
        # Throttle updates to prevent overwhelming clients
        now = time.time()
        throttle_key = f"{update_type}_{target_group or 'all'}"
        
        if throttle_key in self.update_throttle:
            if now - self.update_throttle[throttle_key] < self.throttle_interval:
                return  # Skip this update
        
        self.update_throttle[throttle_key] = now
        
        # Optimize data for streaming
        optimized_data = self.data_optimizer.optimize_data_for_streaming(data)
        
        message = {
            "type": update_type,
            "timestamp": now,
            "data": optimized_data
        }
        
        # Send via WebSocket
        if target_group:
            await self.websocket_manager.broadcast_to_group(target_group, message)
        else:
            await self.websocket_manager.broadcast_to_all(message)
    
    async def create_optimized_websocket_handler(self, websocket: WebSocket, connection_id: str, group: Optional[str] = None):
        """Create an optimized WebSocket handler."""
        if not await self.websocket_manager.connect(websocket, connection_id, group):
            return
        
        try:
            # Send initial connection message
            await self.websocket_manager.send_message(connection_id, {
                "type": "connection_established",
                "connection_id": connection_id,
                "timestamp": time.time()
            })
            
            # Handle incoming messages
            while True:
                try:
                    message = await asyncio.wait_for(websocket.receive_text(), timeout=30.0)
                    
                    # Handle ping/pong for keep-alive
                    if message == "ping":
                        await websocket.send_text("pong")
                    
                    # Update last activity
                    if connection_id in self.websocket_manager.connection_metrics:
                        self.websocket_manager.connection_metrics[connection_id].last_activity = time.time()
                        
                except asyncio.TimeoutError:
                    # Send ping to check if connection is alive
                    await websocket.send_text("ping")
                    
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {connection_id}")
        except Exception as e:
            logger.error(f"WebSocket error for {connection_id}: {e}")
        finally:
            await self.websocket_manager.disconnect(connection_id, group)
    
    async def create_optimized_sse_handler(self, request: Request, stream_id: str, data_generator: Callable):
        """Create an optimized SSE handler."""
        
        async def optimized_generator():
            """Optimized event generator."""
            try:
                async for data in data_generator():
                    if await request.is_disconnected():
                        break
                    
                    # Optimize data for streaming
                    optimized_data = self.data_optimizer.optimize_data_for_streaming(data)
                    
                    yield {
                        "timestamp": time.time(),
                        "data": optimized_data
                    }
                    
                    # Brief pause to prevent overwhelming
                    await asyncio.sleep(0.01)
                    
            except Exception as e:
                logger.error(f"SSE generator error: {e}")
                yield {"error": str(e)}
        
        return await self.sse_manager.create_stream(stream_id, optimized_generator)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get comprehensive performance statistics."""
        return {
            "websocket_stats": self.websocket_manager.get_connection_stats(),
            "sse_stats": self.sse_manager.get_stream_stats(),
            "throttle_stats": {
                "active_throttles": len(self.update_throttle),
                "throttle_interval": self.throttle_interval
            }
        }
    
    async def cleanup_resources(self):
        """Clean up resources for performance."""
        # Clean up stale WebSocket connections
        websocket_cleaned = await self.websocket_manager.cleanup_stale_connections()
        
        # Clean up old throttle entries
        current_time = time.time()
        old_throttles = [
            key for key, timestamp in self.update_throttle.items()
            if current_time - timestamp > 60  # Remove throttles older than 1 minute
        ]
        
        for key in old_throttles:
            del self.update_throttle[key]
        
        # Clean up data optimizer cache
        if len(self.data_optimizer.serialization_cache) > 500:
            # Keep only the most recent 500 entries
            cache_items = list(self.data_optimizer.serialization_cache.items())
            self.data_optimizer.serialization_cache = dict(cache_items[-500:])
        
        logger.info(f"Cleaned up {websocket_cleaned} WebSocket connections and {len(old_throttles)} throttle entries")


# Global optimizer instance
_global_optimizer = RealTimeUpdateOptimizer()


def get_global_optimizer() -> RealTimeUpdateOptimizer:
    """Get the global real-time update optimizer."""
    return _global_optimizer


async def optimize_real_time_performance():
    """Apply real-time performance optimizations."""
    optimizer = get_global_optimizer()
    
    # Start cleanup task
    async def cleanup_task():
        while True:
            await asyncio.sleep(300)  # Clean up every 5 minutes
            await optimizer.cleanup_resources()
    
    asyncio.create_task(cleanup_task())
    
    logger.info("Real-time performance optimizations applied")


if __name__ == "__main__":
    async def test_websocket_performance():
        """Test WebSocket performance."""
        manager = OptimizedWebSocketManager(max_connections=10)
        
        # Simulate connections and messages
        for i in range(5):
            connection_id = f"test_conn_{i}"
            # Note: This is a simplified test - in real usage, you'd have actual WebSocket objects
            manager.connections[connection_id] = None  # Placeholder
            manager.connection_metrics[connection_id] = ConnectionMetrics(
                connection_id=connection_id,
                connection_type="websocket",
                connected_at=time.time(),
                messages_sent=0,
                bytes_sent=0,
                last_activity=time.time(),
                errors=0
            )
        
        # Simulate message sending
        for i in range(100):
            await asyncio.sleep(0.01)
            # In real usage, this would send actual messages
            for connection_id in manager.connections:
                metrics = manager.connection_metrics[connection_id]
                metrics.messages_sent += 1
                metrics.bytes_sent += 100
                metrics.last_activity = time.time()
        
        # Print stats
        stats = manager.get_connection_stats()
        print("WebSocket Performance Test Results:")
        print(f"Active connections: {stats['active_connections']}")
        print(f"Total messages sent: {stats['messages_sent']}")
        print(f"Total bytes sent: {stats['bytes_sent']}")
        
        for conn_id, metrics in stats['connection_metrics'].items():
            print(f"{conn_id}: {metrics['messages_per_second']:.1f} msg/s, {metrics['bytes_per_second']:.1f} bytes/s")
    
    asyncio.run(test_websocket_performance())
