# 🦙🐝 Llama-Bee Metadata System

## Overview

Each LLM (Llama) in the HIVE system has an accompanying BEE metadata that follows it, providing context, capabilities, and choreography instructions. This creates a llama-friendly HIVE where each model knows its role in the swarm.

## Metadata Structure

```json
{
  "bee": {
    "id": "bee-7f3a9c",
    "llama": {
      "model": "gpt-4",
      "provider": "openai",
      "temperature": 0.7,
      "max_tokens": 2000
    },
    "role": {
      "type": "architect",
      "specialization": "decomposition",
      "ring_level": 1
    },
    "dance": {
      "pattern": "waggle",
      "intensity": 0.8,
      "direction": "task_breakdown"
    },
    "swarm": {
      "hive_id": "hive-main",
      "colony": "dev-tools",
      "neighbors": ["bee-4d2f1a", "bee-9e8b3c"]
    },
    "nectar": {
      "tokens_collected": 1523,
      "tokens_saved": 4821,
      "efficiency_rating": 0.76
    }
  }
}
```

## Visual Representation in the Visualizer

```
┌─────────────────────────────────────────────────────┐
│             🦙 Llama Colony Status 🐝               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐│
│  │🦙 GPT-4     │  │🦙 Claude-3  │  │🦙 Mixtral   ││
│  │🐝 Architect │  │🐝 Chronicler│  │🐝 Scout     ││
│  │             │  │             │  │             ││
│  │ ≋≋≋≋≋≋≋≋≋  │  │ ∿∿∿∿∿∿∿∿∿  │  │ ⟳⟳⟳⟳⟳⟳⟳⟳⟳  ││
│  │ Waggle: 8/10│  │ Circle: 6/10│  │ Scout: 9/10 ││
│  │ Nectar: 76% │  │ Nectar: 82% │  │ Nectar: 91% ││
│  └─────────────┘  └─────────────┘  └─────────────┘│
│                                                     │
│         Current Swarm Communication                 │
│  ╭─────────────────────────────────────────╮      │
│  │ 🦙🐝 GPT-4: "Breaking down OAuth task..." │      │
│  │ 🦙🐝 Claude: "Documenting approach..."   │      │
│  │ 🦙🐝 Mixtral: "Found similar patterns!"  │      │
│  ╰─────────────────────────────────────────╯      │
└─────────────────────────────────────────────────────┘
```

## Bee Behavior Patterns

### Dance Types
```python
class BeeDance(Enum):
    WAGGLE = "waggle"          # Complex task communication
    ROUND = "round"            # Simple task notification  
    TREMBLE = "tremble"        # Error or issue alert
    SCOUT = "scout"            # Exploration pattern
    CONVERGE = "converge"      # Consensus building
    DISPERSE = "disperse"      # Parallel execution
```

### Implementation
```python
class LlamaBee:
    """Metadata companion for each LLM"""
    
    def __init__(self, llama_config: Dict):
        self.id = f"bee-{uuid.uuid4().hex[:6]}"
        self.llama = llama_config
        self.dance_pattern = None
        self.nectar_collected = 0
        self.nectar_saved = 0
        
    def perform_dance(self, task_type: str) -> BeeDance:
        """Determine appropriate dance for task"""
        dance_map = {
            "decompose": BeeDance.WAGGLE,
            "document": BeeDance.ROUND,
            "debug": BeeDance.TREMBLE,
            "explore": BeeDance.SCOUT,
            "plan": BeeDance.CONVERGE,
            "execute": BeeDance.DISPERSE
        }
        self.dance_pattern = dance_map.get(task_type, BeeDance.ROUND)
        return self.dance_pattern
        
    def collect_nectar(self, tokens_used: int, tokens_saved: int):
        """Track token efficiency"""
        self.nectar_collected += tokens_used
        self.nectar_saved += tokens_saved
        
    @property
    def efficiency_rating(self) -> float:
        """Calculate bee's efficiency"""
        total = self.nectar_collected + self.nectar_saved
        return self.nectar_saved / total if total > 0 else 0
        
    def to_metadata(self) -> Dict:
        """Export bee metadata"""
        return {
            "bee": {
                "id": self.id,
                "llama": self.llama,
                "dance": {
                    "pattern": self.dance_pattern.value if self.dance_pattern else None,
                    "intensity": self.efficiency_rating
                },
                "nectar": {
                    "tokens_collected": self.nectar_collected,
                    "tokens_saved": self.nectar_saved,
                    "efficiency_rating": self.efficiency_rating
                }
            }
        }
```

## Visualizer Integration

```python
def render_llama_colony(self):
    """Render the llama colony with their bee companions"""
    st.subheader("🦙 Llama Colony Status 🐝")
    
    colonies = asyncio.run(self.get_llama_colonies())
    
    # Create columns for each active llama-bee pair
    cols = st.columns(min(len(colonies), 4))
    
    for idx, (col, colony) in enumerate(zip(cols, colonies)):
        with col:
            # Llama info
            st.markdown(f"### 🦙 {colony['llama']['model']}")
            st.markdown(f"**🐝 {colony['bee']['role']}**")
            
            # Dance visualization
            dance = colony['bee']['dance']['pattern']
            intensity = colony['bee']['dance']['intensity']
            
            # Show dance pattern
            if dance == "waggle":
                st.markdown("≋≋≋≋≋≋≋≋≋")
            elif dance == "round":
                st.markdown("∿∿∿∿∿∿∿∿∿")
            elif dance == "scout":
                st.markdown("⟳⟳⟳⟳⟳⟳⟳⟳⟳")
            elif dance == "tremble":
                st.markdown("≈≈≈≈≈≈≈≈≈")
                
            # Metrics
            st.progress(intensity, text=f"Nectar: {intensity:.0%}")
            
            # Activity indicator
            if colony['active']:
                st.success("🟢 Active", icon="✅")
            else:
                st.info("⚪ Idle", icon="💤")
```

## Swarm Choreography

```python
class SwarmChoreographer:
    """Orchestrate bee dances for coordinated tasks"""
    
    def __init__(self):
        self.colonies = {}
        self.active_dances = []
        
    async def choreograph_task(self, task: Dict) -> List[LlamaBee]:
        """Assign bees and choreograph their dance"""
        task_type = task["type"]
        complexity = task["complexity"]
        
        # Select appropriate llamas and create bees
        if complexity > 8:
            # Complex task needs waggle dance
            lead_bee = self.assign_bee("gpt-4", BeeDance.WAGGLE)
            support_bees = [
                self.assign_bee("claude-3", BeeDance.CONVERGE),
                self.assign_bee("gpt-3.5", BeeDance.ROUND)
            ]
        else:
            # Simple task can use round dance
            lead_bee = self.assign_bee("gpt-3.5", BeeDance.ROUND)
            support_bees = []
            
        # Coordinate the dance
        dance_plan = {
            "lead": lead_bee,
            "support": support_bees,
            "pattern": self.generate_dance_pattern(task_type),
            "duration": self.estimate_dance_duration(complexity)
        }
        
        return dance_plan
```

## Benefits

1. **Visual Metaphor**: Makes AI coordination intuitive
2. **Role Clarity**: Each llama-bee knows its purpose
3. **Efficiency Tracking**: Nectar metaphor for token savings
4. **Debugging**: See which bees are dancing (working)
5. **Educational**: Students understand swarm behavior

## Future Extensions

1. **Pollen Types**: Different data types as pollen
2. **Hive Temperature**: System load visualization
3. **Queen Bee**: Central coordinator role
4. **Seasonal Patterns**: Time-based behavior changes
5. **Cross-Pollination**: Knowledge transfer between models