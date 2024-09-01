# aws-step-f-learning

This is for learning AWS States language and iteration inside step functions.

## Documentation for the states language

https://states-language.net/

## Output Filtering/ Metadata culling: What is the purpose of this code? 
```
"OutputPath": "$.Payload",
```
This restricts the output data set into the State machine to only the application output. Without the above line, all the system meta-data will also be added along with the application data

Similarly, we have this inside the map/ parallel processing task
```
"OutputPath": "$.Payload.body.square",
```
This filters down the output of the parallel processing stage to 
```
[
  7396,
  2116,
  1521,
  196,
  3025
]
```
Instead, if we had this line of code
```
"OutputPath": "$.Payload",
```
we would see the task generating output like this
```
[
  {
    "statusCode": 200,
    "body": {
      "square": 1089
    }
  },
  {
    "statusCode": 200,
    "body": {
      "square": 1444
    }
  },
  {
    "statusCode": 200,
    "body": {
      "square": 8649
    }
  },
  {
    "statusCode": 200,
    "body": {
      "square": 784
    }
  },
  {
    "statusCode": 200,
    "body": {
      "square": 49
    }
  }
] 
```



## What is the purpose of this code, insided the parameters block?
```
"Payload.$": "$",
```
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

The below construct achieves the same as above

```
"Type": "Map",
"InputPath": "$.body",
"ItemsPath": "$.randomList",
```

## Input Structure Refactoring: What is the purpose of the below line of code, contained within the subsequent block?

```
"number.$": "$"
```

inside

```
          "SquareNumbers": {
            "Type": "Task",
            "Resource": "arn:aws:states:::lambda:invoke",
            "OutputPath": "$.Payload.body.square",
            "Parameters": {
              "FunctionName": "arn:aws:lambda:us-east-1:819215969217:function:NumberSquarer:$LATEST",
              "Payload": {
                "number.$": "$"
              }
            }
```

Answer: It transforms the loop value of the iteration into the format that the Lambda wants.

1. The map state itself gets a list of numbers like [2, 33, 7......]
2. Each iteration of this list by itself will create an input like {2}, {33}, {7} ...
3. That line will refactor this input such that, each invocation of the lambda will receive a dict like {"number": 2}, {"number": 33}, {"number": 7} ...







 


## Map state processing modes

Inline – Limited-concurrency mode. In this mode, each iteration of the Map state runs in the context of the workflow that contains the Map state. Step Functions adds the execution history of these iterations to the parent workflow's execution history. By default, Map states run in Inline mode.

In this mode, the Map state accepts only a JSON array as input. Also, this mode supports up to 40 concurrent iterations.


Distributed – High-concurrency mode. In this mode, the Map state runs each iteration as a child workflow execution, which enables high concurrency of up to 10,000 parallel child workflow executions. Each child workflow execution has its own, separate execution history from that of the parent workflow.

In this mode, the Map state can accept either a JSON array or an Amazon S3 data source, such as a CSV file, as its input.

