from services.agents.visualization_agent import (
    VisualizationAgent
)

print(
    VisualizationAgent
    .suggest_visualization(
        "What is total GST amount?"
    )
)

print(
    VisualizationAgent
    .suggest_visualization(
        "Show monthly GST trend"
    )
)

print(
    VisualizationAgent
    .suggest_visualization(
        "Compare vendor spending"
    )
)