Cellscope Infrastructure
========================

Biomage Cellscope is a single-cell RNA sequencing data analysis platform that is served in a Software-as-a-Service manner. As such, we use and embrace the [cloud-native](https://en.wikipedia.org/wiki/Cloud_native_computing) development paradigm in order to provide our users with a scalable, resilient, and highly available service to the greatest extent possible.

Design paradigms
----------------

We try to abide by the a set of paradigms when designing Biomage infrastructure. You can see this reflected in the architecture we currently have as well as the direction in which future development goes. When designing a new piece of infrastructure for Biomage, we have found it easy to narrow down potential options by observing a few key considerations. Make sure you observe the following paradigms, in order from most to least important.

The Cellscope technology stack should:

* __be AWS-native__: Engineering work at Biomage is done by a small team of engineers, bioinformaticians, managers, and other professionals. We have really good in-house knowledge of Amazon Web Services. In order to scale a platform to the extent we want to, we need everyone to write code instead of managing complex infrastructure. As such, infrastructure should be native to AWS unless it is absolutely unavoidable. AWS has a rich set of native tools that should be suitable for most tasks. When multiple AWS-native tools meet requirements, choose the one that is fully managed and requires the least configuration. For example, prefer [DynamoDB](https://aws.amazon.com/dynamodb/) over[DocumentDB](https://aws.amazon.com/documentdb/).

* __be cloud-native__: When no AWS tool meets the requirements, or they need to be augmented in a custom way, the infrastructure should be cloud-native. As a good rule of thumb, it should be able to be deployed using a container orchestrator like Kubernetes and provide high availability, scalability, and resiliency out of the box while it is deployed.

* __use what's popular__: If in doubt, use the tool that most people use. Tools with larger, active, vibrant communities have better support, with an extensive knowledge base available on the internet. It is better to use a more popular and less technologically advanced solution than one with fewer users that meet your requirements perfectly.

* __put user experience first__: Existing tools will often have bad performance or unacceptable drawbacks when it comes to serving an interactive application with large data sets. When choosing a piece of infrastructure, remember to understand the needs of the user and put their needs first. It is better to design a system that is more complicated but provides a better experience for the end user in a critical part of the system.

* __come together nicely__: The paradigms above already encompass this somewhat: AWS-native, clud-native and popular tools are often easy to integrate and work with, but sometimes different tools integrate with existing infrastructure in a better, more coherent way. If this happens, use the technology that will integrate better into the existing system.

Directory
---------

Almost all of the Cellscope stack is managed using an [Infrastructure as Code](https://en.wikipedia.org/wiki/Infrastructure_as_code) paradigm. Resources are typically defined using configuration files that are modified in a pull request, and applied to the system using Continuous Deployment when the request is approved and merged. This serves as a resource for engineers looking to find the definitions to certain resources:

### Deploying Cellscope

Almost the entirety of Biomage can be brought up from scratch using Continuous Deployment. The action [Deploy Biomage infrastruture](https://github.com/hms-dbmi-cellenics/iac/actions/workflows/deploy-infra.yaml) is responsible for this task. This must be manually triggered by someone with administrator/root access to the cluster for any changes to be applied. Deploying is non-destructive and so can be done as much as desired.

The exact pipeline is found at [iac/.github/workflows/deploy-infra.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/.github/workflows/deploy-infra.yaml). The file is a GitHub actions configuration and documentation for it is found [here](https://docs.github.com/en/actions). PRs to this file will be approved and merged in by someone with root rights to AWS.

### Kubernetes cluster settings

Kubernetes is managed using [eksctl](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html). The cluster configuration file is located under [iac at cf/cluster.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/infra/cluster.yaml), and includes things like the number of nodes deployed, their size, the type of AWS technologies to enable on the cluster, etc. Changes can be made and a PR created, which must be merged in and approved with someone with root rights to the AWS account.

Note: per the eksctl documentation, node groups are immutable. If you want to change the node group type, storage size, or any other property, you must delete the old node group from the configuration, and add a new one with a different name. eksctl will then appropriately drain and set up node groups.

### AWS resources

AWS resources, such as S3 buckets, SQS queues, SNS topics, DynamoDB tables, etc., are stored under [iac/cf/*](https://github.com/hms-dbmi-cellenics/iac/tree/master/cf) as [CloudFormation](https://aws.amazon.com/cloudformation/) files. All CloudFormation files must have a mandatory `Environment` parameter, which can be either `development`, `staging`, or `production`. Changes made to these files can be submitted as a PR. When they are merged in, a GitHub action under [iac/.github/workflows/deploy-changed-cf.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/.github/workflows/deploy-changed-cf.yaml) deploys them to AWS on both environments. In addition, this action is also run in a dry-run mode when the merge request is created on any file under `iac/cf/*` to verify the file.

There are also certain "stationary" AWS resources that cannot be managed in such a manner and a [re-deploy](#deploying-cellscope) is necessary. These are found under `iac/infra/cf-*.yaml`. This includes a secret key used to send sensitive information to GitHub Actions publicly at [iac/infra/cf-iac-secret-key.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/infra/cf-iac-secret-key.yaml). These are deployed using steps created in [iac/.github/workflows/deploy-infra.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/.github/workflows/deploy-infra.yaml) and as such changes to them need to be applied by [re-deploying](#deploying-cellscope) Cellscope.

### AWS permissions for developers

Access to AWS resources at Biomage is managed using [CloudFormation](https://aws.amazon.com/cloudformation/). Files of the format `iac/cf/*-access-group.yaml` are used to define groups with certain permissions that are applied to employees. For example, the engineer roles are found at [iac/cf/developer-access-group.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/cf/developer-access-group.yaml). They behave exactly like any other [AWS resource](#aws-resources).

### AWS permissions for code in staging/production

AWS permissions work slightly different for Kubernetes resources such as code running in the Kubernetes cluster in production. These use an AWS facility called IAM Roles for Service Accounts (IRSA), and are found under `iac/cf/irsa-*-role.yaml`, where `*` is the name of the repository where code is running from.

More information about IRSA can be found [here](https://docs.aws.amazon.com/eks/latest/userguide/create-service-account-iam-policy-and-role.html) and [here](https://docs.aws.amazon.com/eks/latest/userguide/specify-service-account-role.html).

For example, the rights granted to the api service running in staging or production is found at [iac/cf/irsa-api-role.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/cf/irsa-api-role.yaml). As a general rule, services are run using service accounts named `deployment-runner`, and therefore the accounts the role apply to are of the format `system:serviceaccount:api-*:deployment-runner`, as seen in the file. Everything else related to [AWS resources](#aws-resources) still applies.

### Kubernetes permissions for users and AWS resources

Kubernetes has a different permissions system than AWS and the two interoperate rather poorly. In order to give a certain IAM user or IAM role certain permissions to perform actions on Kubernetes, such as connect to Kubernetes, create resources, read logs, etc., AWS uses [IAM Identity Mappings](https://docs.aws.amazon.com/eks/latest/userguide/add-user-role.html). These are rights *granted on the Kubernetes cluster* to *AWS users and roles*, and require special setup. We use eksctl and its [identity mappings support](https://eksctl.io/usage/iam-identity-mappings/).

__For IAM users such as developers__: The files [iac/infra/cluster_admins_production](https://github.com/hms-dbmi-cellenics/iac/blob/master/infra/cluster_admins_production), [iac/infra/cluster_admins_staging](https://github.com/hms-dbmi-cellenics/iac/blob/master/infra/cluster_admins_staging), [iac/infra/cluster_users](https://github.com/hms-dbmi-cellenics/iac/blob/master/infra/cluster_users) contain names on each line of IAM users who have respective rights on the cluster. These files can be modified and a PR raised for them. Note: the file must end with a newline character.

When approved, Cellscope must be [re-deployed](#deploying-cellscope). As seen in that directory entry, the GitHub action under [iac/.github/workflows/deploy-infra.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/.github/workflows/deploy-infra.yaml) is deployed, where steps `update-identitymapping-admin` and `update-identitymapping` deal with reading the files and adding these users to the list as administrators.

__For IAM roles such as AWS Step Function executions, EC2 instances, etc.__: Access to cluster can be managed by directly editing [iac/.github/workflows/deploy-infra.yaml](https://github.com/hms-dbmi-cellenics/iac/blob/master/.github/workflows/deploy-infra.yaml) and [re-deploying](#deploying-cellscope). See step `add-state-machine-role` that adds the IAM role `state-machine-role-[staging/production]` certain rights.

### Docker images

Docker images can be found in AWS ECR at [https://eu-west-1.console.aws.amazon.com/ecr/]. Each GitHub repository has a corresponding ECR repository where images from builds are pushed. For example, the [ui](https://github.com/hms-dbmi-cellenics/ui) repository on GitHub has a corresponding [ECR registry](https://eu-west-1.console.aws.amazon.com/ecr/repositories/private/242905224710/ui?region=eu-west-1), and images can be pulled using Docker from `242905224710.dkr.ecr.eu-west-1.amazonaws.com`, where `242905224710` is the account ID for the AWS account.

Images use immutable tags and therefore there is no `latest` tag. Images are tagged according to the following scheme:

* the fully resolved Git ref, with all slashes (`/`) replaced by dashes (`-`)
* a dash (`-`)
* followed by the commit's full checksum.

Thus, to find the image created by [this](https://github.com/hms-dbmi-cellenics/ui/commit/b531d371bd79c64439e76769dfb49cccd4d14fc6) commit, we note that:

* the repository name is `ui`
* the commit was pushed to `master`, the fully qualified ref being `refs/heads/master`
* the commit's checksum is `b531d371bd79c64439e76769dfb49cccd4d14fc6`.

Therefore, the image can be found under the tag `refs-heads-master-b531d371bd79c64439e76769dfb49cccd4d14fc6` in the AWS console and can be fetched using the image URL `http://242905224710.dkr.ecr.eu-west-1.amazonaws.com/ui:refs-heads-master-b531d371bd79c64439e76769dfb49cccd4d14fc6`.

Some repositories, such as [worker](https://github.com/hms-dbmi-cellenics/worker) and [pipelines](https://github.com/hms-dbmi-cellenics/pipeline) create multiple images during the build process. These are tagged in a similar way, except additional text is appended to the end of the tag following a dash (`-`).

For example, [this](https://github.com/hms-dbmi-cellenics/worker/commit/9985ae28463678cad185c288ff26153c0d2a712d) commit produced four individual images, called:

* `242905224710.dkr.ecr.eu-west-1.amazonaws.com/worker:refs-heads-master-9985ae28463678cad185c288ff26153c0d2a712d-r`
* `242905224710.dkr.ecr.eu-west-1.amazonaws.com/worker:refs-heads-master-9985ae28463678cad185c288ff26153c0d2a712d-r-builder`
* `242905224710.dkr.ecr.eu-west-1.amazonaws.com/worker:refs-heads-master-9985ae28463678cad185c288ff26153c0d2a712d-python`
* `242905224710.dkr.ecr.eu-west-1.amazonaws.com/worker:refs-heads-master-9985ae28463678cad185c288ff26153c0d2a712d-python-builder`

### Details of code running in staging/production

TBA
