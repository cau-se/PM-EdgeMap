# The PM-EdgeMap

The process mining edge map (PM-EdgeMap) helps evaluating and running process mining algorithms on a simulated 
edge-cloud continuum. 

## Usage
To run the PM-Edge map you can run the main as shown below:

```python
simulator = Simulator(
    topology_directory="topology",
    result_directory="results"
)

simulator.run(
    algorithm=lambda: EdgeConformanceCheckingAlgorithm(learning_events=100),
    topology_key="mec",
    metric_name="metric-data-network-resource",
    metrics=["data-network-resource"],
    velocity=100,
    evaluation_batch=100
)
```
### Parameters
`topologyKey`: references the name of the topology description yaml-file,
`metric_name`: name to reference the result file for the analysis,
`metrics`: name of the evaluated metric,
`velocity`: Number of simulated events emitted per time unit,
`evaluation batch`: Batch to evaluate the resource consumption to be robust to peeks,


