# HIVE Visualizer Module - Ring 4

## Overview

The HIVE Visualizer is a Ring 4 module that provides real-time visualization of the HIVE system's activity, showing the ring architecture, active modules, swarm communications, and performance metrics through an interactive Streamlit dashboard.

## Visual Design Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                    🐝 HIVE System Visualizer 🐝                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │   Ring Status   │  │  Active Swarms   │  │ Word Cloud    │ │
│  │                 │  │                  │  │               │ │
│  │  Ring 0: ████  │  │  🐝 OAuth Task   │  │  decompose    │ │
│  │  Ring 1: ████  │  │  🐝 Sprint Plan  │  │    sprint     │ │
│  │  Ring 2: ███░  │  │  🐝 Doc Gen     │  │  analyze API  │ │
│  │  Ring 3: ██░░  │  │                  │  │    tokens     │ │
│  │  Ring 4: ████  │  │  12 agents active│  │  performance  │ │
│  └─────────────────┘  └──────────────────┘  └───────────────┘ │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    Live Ring Topology                    │   │
│  │                                                          │   │
│  │                      ┌─────────┐                         │   │
│  │                 ┌────│ Ring 0  │────┐                    │   │
│  │                 │    └────┬────┘    │                    │   │
│  │            ┌────▼───┐    │    ┌────▼───┐                │   │
│  │            │Ring 1.1│    │    │Ring 1.2│                │   │
│  │            └────┬───┘    │    └────┬───┘                │   │
│  │         ┌───────▼────────▼─────────▼──────┐             │   │
│  │         │          Ring 2 Modules          │             │   │
│  │         └──────────────┬──────────────────┘             │   │
│  │                        │                                 │   │
│  │                 [Animated flow lines]                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  Performance Metrics                     │   │
│  │                                                          │   │
│  │  Requests/sec: ▁▂▄█▆▄▂▁  Token Usage: ▁▃▆█▅▃▁          │   │
│  │  Latency (ms): 45 avg     Efficiency: 73% saved         │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation

### Module Structure
```python
# hive_visualizer/module.py
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import asyncio
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from typing import Dict, List, Optional

class HiveVisualizerModule(HiveModule):
    """Interactive visualization of HIVE system activity"""
    
    def __init__(self):
        super().__init__(ring_level=4)
        self.dependencies = ["event_bus", "metrics_collector", "module_registry"]
        self.provided_tools = [
            "visualizer:snapshot",
            "visualizer:stream", 
            "visualizer:replay"
        ]
        self.activity_buffer = []
        self.word_frequency = {}
        
    async def initialize(self, core_services: Dict) -> None:
        self.event_bus = core_services["event_bus"]
        self.metrics = core_services["metrics_collector"]
        self.registry = core_services["module_registry"]
        
        # Subscribe to all system events
        await self.event_bus.subscribe("tool:invoked", self.on_tool_invoked)
        await self.event_bus.subscribe("module:loaded", self.on_module_loaded)
        await self.event_bus.subscribe("swarm:spawned", self.on_swarm_spawned)
        
    def create_streamlit_app(self):
        """Create the Streamlit dashboard"""
        st.set_page_config(
            page_title="HIVE System Visualizer",
            page_icon="🐝",
            layout="wide"
        )
        
        st.title("🐝 HIVE System Visualizer")
        
        # Create layout columns
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            self.render_ring_status()
            
        with col2:
            self.render_ring_topology()
            
        with col3:
            self.render_active_swarms()
            
        # Full width sections
        self.render_activity_stream()
        self.render_performance_metrics()
        
    def render_ring_status(self):
        """Render ring health status panel"""
        st.subheader("Ring Status")
        
        ring_data = asyncio.run(self.get_ring_status())
        
        for ring_num, status in ring_data.items():
            modules = status["modules"]
            active = status["active"]
            total = status["total"]
            health = status["health"]
            
            # Create progress bar
            progress = active / total if total > 0 else 0
            color = "green" if health == "healthy" else "orange"
            
            st.metric(
                label=f"Ring {ring_num}",
                value=f"{active}/{total} modules",
                delta=f"{health}"
            )
            st.progress(progress)
            
    def render_ring_topology(self):
        """Render interactive ring topology diagram"""
        st.subheader("Live Ring Topology")
        
        # Create hierarchical graph
        fig = go.Figure()
        
        # Get current topology
        topology = asyncio.run(self.get_system_topology())
        
        # Add nodes for each ring
        for ring_num, modules in topology["rings"].items():
            # Calculate positions in circle
            angle_step = 2 * np.pi / len(modules) if modules else 0
            radius = (ring_num + 1) * 50
            
            for i, module in enumerate(modules):
                angle = i * angle_step
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers+text',
                    name=module["name"],
                    text=[module["name"]],
                    textposition="top center",
                    marker=dict(
                        size=20,
                        color=self._get_ring_color(ring_num),
                        line=dict(width=2, color='white')
                    ),
                    showlegend=False
                ))
        
        # Add connections between modules
        for connection in topology["connections"]:
            fig.add_trace(go.Scatter(
                x=[connection["from"]["x"], connection["to"]["x"]],
                y=[connection["from"]["y"], connection["to"]["y"]],
                mode='lines',
                line=dict(
                    width=2,
                    color='rgba(125, 125, 125, 0.5)'
                ),
                showlegend=False
            ))
        
        # Update layout
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    def render_active_swarms(self):
        """Show currently active swarm agents"""
        st.subheader("Active Swarms")
        
        swarms = asyncio.run(self.get_active_swarms())
        
        for swarm in swarms[:5]:  # Show top 5
            with st.container():
                st.write(f"🐝 **{swarm['task']}**")
                st.caption(f"Agents: {swarm['agent_count']} | Started: {swarm['started']}")
                st.progress(swarm['progress'])
                
        st.metric("Total Active Agents", len(swarms))
        
    def render_activity_stream(self):
        """Render real-time activity word cloud"""
        st.subheader("Activity Word Cloud")
        
        # Generate word cloud from recent activities
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            colormap='viridis'
        ).generate_from_frequencies(self.word_frequency)
        
        # Display using matplotlib
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        
        # Activity ticker
        st.subheader("Recent Activity")
        activity_container = st.container()
        
        with activity_container:
            for activity in self.activity_buffer[-10:]:
                st.text(f"{activity['timestamp']} - {activity['tool']} - {activity['summary']}")
                
    def render_performance_metrics(self):
        """Render performance metrics charts"""
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = asyncio.run(self.get_performance_metrics())
        
        with col1:
            st.metric(
                "Requests/sec",
                f"{metrics['requests_per_sec']:.1f}",
                f"{metrics['requests_delta']:+.1f}"
            )
            
        with col2:
            st.metric(
                "Avg Latency",
                f"{metrics['avg_latency']:.0f}ms",
                f"{metrics['latency_delta']:+.0f}ms"
            )
            
        with col3:
            st.metric(
                "Token Efficiency",
                f"{metrics['token_efficiency']:.0%}",
                f"{metrics['efficiency_delta']:+.1%}"
            )
            
        with col4:
            st.metric(
                "Active Connections",
                metrics['active_connections'],
                f"{metrics['connection_delta']:+d}"
            )
        
        # Time series charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Request rate chart
            fig = px.line(
                metrics['timeseries'],
                x='timestamp',
                y='requests_per_sec',
                title='Request Rate Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            # Token usage chart
            fig = px.area(
                metrics['timeseries'],
                x='timestamp',
                y='tokens_saved',
                title='Tokens Saved Over Time'
            )
            st.plotly_chart(fig, use_container_width=True)
            
    # Event handlers
    async def on_tool_invoked(self, event: Dict) -> None:
        """Handle tool invocation events"""
        tool_name = event["data"]["tool"]
        
        # Update word frequency
        words = tool_name.split(":")
        for word in words:
            self.word_frequency[word] = self.word_frequency.get(word, 0) + 1
            
        # Add to activity buffer
        self.activity_buffer.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "tool": tool_name,
            "summary": event["data"].get("summary", "Processing...")
        })
        
        # Keep buffer size manageable
        if len(self.activity_buffer) > 100:
            self.activity_buffer.pop(0)
            
    def _get_ring_color(self, ring_num: int) -> str:
        """Get color for ring visualization"""
        colors = [
            "#FF6B6B",  # Ring 0 - Red (Core)
            "#4ECDC4",  # Ring 1 - Teal (Essential)
            "#45B7D1",  # Ring 2 - Blue (Extended)
            "#96CEB4",  # Ring 3 - Green (Integration)
            "#FECA57",  # Ring 4 - Yellow (UI)
        ]
        return colors[ring_num] if ring_num < len(colors) else "#95A5A6"
```

### Streamlit App Runner
```python
# hive_visualizer/app.py
import streamlit as st
import asyncio
from hive_visualizer.module import HiveVisualizerModule

# Initialize module
@st.cache_resource
def get_visualizer():
    return HiveVisualizerModule()

def main():
    visualizer = get_visualizer()
    
    # Auto-refresh every 1 second
    st_autorefresh = st.empty()
    
    # Create the dashboard
    visualizer.create_streamlit_app()
    
    # Auto refresh
    with st_autorefresh:
        st.button("Refresh", key="refresh")
        st.write("Auto-refreshing every 1 second...")
        
if __name__ == "__main__":
    # Run with: streamlit run hive_visualizer/app.py
    main()
```

### Docker Configuration
```dockerfile
# Dockerfile.visualizer
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy visualizer module
COPY hive_visualizer/ ./hive_visualizer/

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "hive_visualizer/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Integration with HIVE
```python
# In main HIVE configuration
async def setup_visualizer():
    """Setup visualizer as Ring 4 module"""
    
    # Load visualizer module
    from hive_visualizer.module import HiveVisualizerModule
    await hive.registry.load_module(HiveVisualizerModule)
    
    # Start Streamlit in subprocess
    import subprocess
    subprocess.Popen([
        "streamlit", "run", 
        "hive_visualizer/app.py",
        "--server.port=8501",
        "--server.headless=true"
    ])
    
    print("HIVE Visualizer available at http://localhost:8501")
```

## Demo Features

### 1. Ring Activity Animation
- Pulsing rings when modules are active
- Connection lines animate when data flows
- Color intensity shows load

### 2. Swarm Choreography View
- See agents "dance" as they coordinate
- Waggle patterns for different task types
- Formation changes during execution

### 3. Token Savings Counter
- Real-time counter showing tokens saved
- Comparison with "traditional" approach
- Celebration animation at milestones

### 4. "Tune In" Feature
- Click on any swarm to see snippets
- Read actual agent communications
- Word cloud updates with agent thoughts

### 5. Performance Heatmap
- Grid showing module performance
- Hot spots indicate heavy usage
- Click to drill down into specific tools

## Benefits of Visualizer Module

1. **Immediate Understanding**: See the ring architecture in action
2. **Debugging Aid**: Spot bottlenecks and failed modules
3. **Demo Power**: Show stakeholders the system's elegance
4. **Team Awareness**: Everyone sees what the system is doing
5. **Performance Insights**: Real-time efficiency metrics

## Future Enhancements

1. **3D Ring Visualization**: WebGL-based 3D ring view
2. **Historical Playback**: Replay system activity
3. **Custom Dashboards**: User-defined metric panels
4. **Alert Configuration**: Visual alert setup
5. **Module Marketplace**: Browse and install new rings

This visualizer brings the HIVE to life, making the token efficiency and swarm coordination visible and tangible!