# aws-step-f-learning

This is for learning AWS States language and iteration inside step functions.

## Documentation for the states language

https://states-language.net/

## What is the purpose of this code? --> "OutputPath": "$.Payload",

This restricts the output data set into the State machine to only the application output. Without the above line, all the system meta-data will also be added along with the application data

## What is the purpose of this code, insided the parameters block? --> "Payload.$": "$",

Based on my experiments, it seems to be redundant. Removing it is causing no effect on the input.

## What is the purpose of these lines of code, inside a parallel processing block?
```
"Type": "Map",
"InputPath": "$.body.randomList",
"ItemsPath": "$",
```

The first line says that this would be a parallel iteration task. 
The second line filters or culls the state input down to just the randomList field inside the body object.
The third line specifies which field should be used for iteration. In this case, we have already used InputPath to narrow the data down to the list. So, iteration can be done directly on what is received; this is specified by $ 
