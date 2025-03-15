Page Topics
-----------

[End-user experience](#product-features#amazon-q-business-expert-features#conversational-interface)[Deployment and management](#product-features#amazon-q-business-expert-features#deployment)[Security and governance](#product-features#amazon-q-business-expert-features#security)[Amazon Q Apps](#product-features#amazon-q-business-expert-features#amazon-q-apps)

End-user experience

End-user experience
-------------------

[Open all](#)

### Conversational experience with generative prompts and tasks

Through a conversational experience, Amazon Q Business finds and synthesizes information from across your enterprise or application. This helps your users have tailored conversations, ask questions and get accurate answers, brainstorm ideas, summarize lengthy reports, generate content, and take actions.

### Sources and references

Amazon Q Business provides references and citations to the sources used to generate its answers, building user trust.

### Start or continue existing conversations

Amazon Q Business can start new conversations or continue an existing dialogue. Users can ask a question, receive a response, and then ask follow-up questions and add new information while keeping the context from the previous answer.

### Quick and easy feedback mechanism

Amazon Q Business provides thumbs-up and thumbs-down buttons for every interaction, so users can give feedback on whether the response was useful or not.

### File upload

Amazon Q Business allows end users to upload files and perform tasks like summarization, Q&A, or data analysis.

### Include answers from databases and data warehouses

Amazon Q Business can provide answers to questions across multimedia data, such as text documents, images, audio, and video files. It can also incorporate data from databases and data warehouses through its integration with Amazon QuickSight. This integration provides users with a single conversational interface that provides comprehensive answers from any enterprise knowledge source.

### Citation snippets

Easily verify the responses from Amazon Q Business using contextual source snippet information associated with the source documents.

### Action integrations

Amazon Q Business provides a ready-to-use library of integrations that allow users to take actions across a number of [third party applications](https://aws.amazon.com/q/business/actions/). Administrators install one plugin for each application that enables multiple actions for that application.

### Custom plugins

With custom plugins, admins can connect any third-party application so that users can use natural language prompts to perform actions like completing a task and sending meeting invites directly through Amazon Q Business. For example, custom plugins can be used to search real-time enterprise data such as employee vacation balances, scheduled meetings, and more.

### Content creation mode

Safely access generative AI models built into Amazon Q Business for creative use cases such as summarization of responses and crafting personalized emails.

### Personalized responses

Amazon Q Personalization uses employee profile data from your organization’s identity provider that you have connected to AWS IAM Identity Center, with no additional setup needed, for contextual, more useful responses.

### Extract insights from visual elements within documents

Amazon Q Business users can get answers from visual elements embedded within documents, including PDF, Microsoft PowerPoint and Word, Google Docs, and Google Slides. To learn more, visit the [documentation](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/extracting-meaning-from-images.html).

### Browser extensions and third-party application integrations

Integrations with third-party applications, such as Slack, Microsoft Outlook and Word for Microsoft 365, Microsoft Teams, and web browsers through extensions for Google Chrome, Mozilla Firefox, and Microsoft Edge, make Amazon Q Business available in the applications to summarize and generate content without the need to switch applications.

Deployment and management
-------------------------

[Open all](#)

### Easy deployment and management

Amazon Q Business handles the heavy lifting for you—there’s no need to manage complex machine learning (ML) infrastructure or models. Amazon Q Business connects to your data using prebuilt connectors that support user access control. It has a built-in semantic document retriever and a ready-to-deploy chat interface for end users to allow for easy deployment on a website or in your application.

### Managed data connectors

Amazon Q Business provides over 40 fully managed connectors that bring data from popular enterprise applications, document repositories, chat applications, and knowledge management systems into a single index. For more information about Amazon Q Business—supported data source connectors, see [Amazon Q connectors](https://aws.amazon.com/q/business/connectors/).

### Extending the Amazon Q index to verified software providers

You can allow your third-party software providers to access the index for your Amazon Q Business environment to provide better context through their own generative AI assistants. [Read more about verified software providers and the Amazon Q index](https://aws.amazon.com/q/software-provider/).

### CloudFormation

Use the Amazon Q business template for AWS CloudFormation to easily automate the creation and provisioning of infrastructure resources.

### Index boosting

Tune the relevance of results by configuring the Amazon Q Business retriever to boost specific fields and attributes to assign more importance to specific responses.

Security and governance
-----------------------

[Open all](#)

### Data and application security

Amazon Q Business supports access control for your data so that users receive the right responses based on their permissions. You can integrate Amazon Q Business with your external SAML 2.0–supported identity provider (such as Okta, Azure AD, and Ping Identity) to manage user authentication and authorization.

### Administrator controls

Amazon Q Business offers administrator controls to enable or disable the following capabilities: (1) Restrict responses to enterprise content only or use its own knowledge to respond to queries when there is no relevant content in the enterprise repository. (2) Define blocked topics. (3) Set the context for optimal responses.

### Single Sign-on

Securely connect your users to Amazon Q Business applications, and centrally manage access through single-sign on using AWS IAM Identity Center or Identity Federation with IAM.

### PrivateLink

Use AWS PrivateLink to access Amazon Q Business securely in your Amazon Virtual Private Cloud (Amazon VPC) environment using a VPC endpoint.

### CloudTrail

Amazon Q Business is integrated with AWS CloudTrail to record actions taken by a user, role, or AWS service in Amazon Q.

### FIPS endpoints

Support is included for Federal Information Processing Standards (FIPS) endpoints, based on the US and Canadian government standards and security requirements for cryptographic modules that protect sensitive information.

Amazon Q Apps
-------------

[Open all](#)

### Create

Rapidly create generative AI-powered, secure, reusable, and customizable apps by describing them in natural language. Transform your existing conversations into apps to use every time you need them. Amazon Q Apps intelligently captures the context, nuances, and specifics of your conversation, translating them into a customized app tailored to your needs.

### Customize

Quickly customize the app layout and add or remove a variety of input, output, forms, and plugin cards that generate content, capture inputs from users, or execute tasks. Users have the option to duplicate and customize apps to fit unique user and business requirements, allowing for personalized versions without compromising the original app.

### Share

Easily share apps privately with one or more users or openly with everyone in the organization. In a few steps, users share apps with selected users to limit access for scenarios such as app testing or specific team-only use, or publish apps in the Amazon Q Apps library for everyone with access to the Amazon Q Business environment to access.

### Integrate

Amazon Q Apps allows you to integrate apps into your other tools or applications you choose through APIs that seamlessly allow you to create and consume the generated outputs.

### Administrate

Maintain data sources, access controls, and guardrails in Amazon Q Business for use in Amazon Q Apps. Users can safely and securely use Amazon Q Apps, as all data sources, associated user permissions, and guardrails are preserved. Administrators can leverage controls to give additional credibility to user apps with app verification, create customized library labels to meet customer-specific organizational requirements, and enable or disable the Amazon Q Apps creation and run features for web experience users.