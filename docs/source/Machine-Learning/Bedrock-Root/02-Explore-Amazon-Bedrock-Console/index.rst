Explore Amazon Bedrock Console
==============================================================================



Playground
------------------------------------------------------------------------------
Playground 是一个类似于 ChatGPT 的界面, 能让你和各种 AI 进行交互. 相当于是一个实验性质的功能. 目前有三种交互模式:

- `Chat <https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/chat-playground>`_: 跟 ChatGPT 一样, 是一个问答 Bot. 下面是官方的说明:

    Use the chat playground to experiment with the Amazon Bedrock chat models. Choose a model and optionally configure the inference parameters. Then, enter a prompt and choose "Run" to view the chat output and metrics.

    You get the following metrics.

    Latency — The time it takes for the model to generate each token (word) in a sequence.
    Input token count — The number of tokens that are fed into the model as input during inference.
    Output token count — The number of tokens generated in response to a prompt. Longer, more conversational, responses require more tokens.
    Cost — The cost of processing the input and generating output tokens.
    Optionally, you can configure a criteria that you want the model metrics to match.

    Turn on "compare mode" to compare the chat output and metrics for up to three chat models.

    At any time, you can reset the inference parameters or matching criteria to their default values.

- `Text <https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/text-playground>`_: 以输出 Text 为目标, 和 Chat 类似, 不过是有更加特定的应用场景, 比如 "Action items from a meeting transcript", "Advanced Q&A with Citation". 下面是官方的说明:

    Use the text playground to experiment with the Amazon Bedrock text generative models.

    Choose a model and optionally configure inference parameters. Then, enter a prompt and choose "Run" to view the text output that the model generates.

    At any time, you can reset the inference parameters to their default values.

- `Image <https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/image-playground>`_: 以输出 Image 为目标. 你可以选择特定的应用场景, 例如文生图, 根据图形生成其他有变化的图. 下面是官方的说明:

    Sse the image playground to experiment with the Amazon Bedrock image models. Choose a model and optionally configure inference parameters and other values. Then, enter a prompt and choose "Run" to view the image that the model generates for the prompt.

    At any time, you can change and reset the configurations for the model.


你可以先选择一个模型, 然后输入一些文本, 看看 AI 的回复.