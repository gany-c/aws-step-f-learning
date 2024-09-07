# aws-step-f-learning

This is for learning AWS States language and iteration inside step functions.

## Documentation for the states language

https://states-language.net/

## Advanced view of the Task states

In the UI. Use the Advanced View to examine Task Inputs and Outputs. Sometimes the regular view doesn't refresh.

## Manipulating the task-level state ('$') and full state ('$$')

'$' gives access to the task level input. This will be illustrated in several examples below.

'$$' will give access to the entire step function invocation input including metadata. 
e.g. this is a way of getting the Step-function's invocation name and passing to the lambda as a parameter calle invocation:

```
 "invocation.$": "$$.Execution.Name"
```

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

1. The map state itself gets a list of numbers like 
```
[2, 33, 7......]
```
2. Each iteration of this list by itself will create an input like 
```
{2}, {33}, {7} ...
```
3. The line "number.$": "$" will refactor this input such that, each invocation of the lambda will receive a dict like 
```
{"number": 2}, {"number": 33}, {"number": 7} ...
```

## Static Inputs

1. You can define static inputs to the tasks/lambdas, the static inputs can also be inside a static json structure:

In the below example, the lambda will always receive an input parameter called illustrative_static_input with value 100. The second parameter is a static nested one.
```
      "Parameters": {
        "Payload": {          
          "illustrative_static_input": 100,
          "illustrative_static_nested_input": {
            "nested_field": "200"
          },
```

## What is the purpose of this code, insided the (input) parameters block?
```
"Payload.$": "$",
```
Based on my experiments, it seems to be redundant. Removing it is causing no effect on the input. The nature of term "Payload" on the input side is not clear. In some versions, it is treated as a keyword and in some versions it is treated as just another input.

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



## Map state processing modes

Inline – Limited-concurrency mode. In this mode, each iteration of the Map state runs in the context of the workflow that contains the Map state. Step Functions adds the execution history of these iterations to the parent workflow's execution history. By default, Map states run in Inline mode.

In this mode, the Map state accepts only a JSON array as input. Also, this mode supports up to 40 concurrent iterations.


Distributed – High-concurrency mode. In this mode, the Map state runs each iteration as a child workflow execution, which enables high concurrency of up to 10,000 parallel child workflow executions. Each child workflow execution has its own, separate execution history from that of the parent workflow.

In this mode, the Map state can accept either a JSON array or an Amazon S3 data source, such as a CSV file, as its input.

