
# S3


## biomage-original-production/[experiment_name]



*   Description: original files from users (barcodes.tsv, genes.tsv, & matrix.mtx)
*   ReadBy: manual, data-upload-production
*   WrittenBy: manual upload
*   Resource: s3


## biomage-original-staging/ Empty


## biomage-source-production/[experiment_id]/r.rds



*   Description: resulting R rds file from data-ingest
*   Format: RDS
*   ReadBy: pipeline-production
*   WrittenBy: data-ingest, data-upload-production, data-processing-production
*   Resource: s3


## biomage-source-staging/[sandbox_id-experiment_id]/r.rds



*   Description: resulting R rds files from deploying a staging environment, the sandbox id is included as key
*   Format: RDS
*   ReadBy: pipeline-staging
*   WrittenBy: stage experiment (biomage-utils), manual
*   Resource: s3


## cell-sets-production/[experiment_id]



*   Description: cell set file created during data ingest
*   Format: JSON
*   ReadBy: pipeline-production, api-production, worker-production
*   WrittenBy: data-ingest, data-upload-production, data-processing-production
*   Resource: s3


## cell-sets-staging/[sandbox_id-experiment_id]



*   Description: cell set file copied during staging
*   Format: JSON
*   ReadBy: pipeline-staging, api-staging, worker-staging
*   WrittenBy:stage experiment (biomage-utils), manual
*   Resource: s3


## plots-tables-production/[plot_UUID]



*   Description: data points displayed in the plots of data processing (the others are in redux) s 
*   Format: JSON
*   ReadBy: api-production
*   WrittenBy: pipeline-production, worker-production
*   Resource: s3


## plots-tables-staging/[plot_UUID]



*   Description: data points displayed in the plots of data processing (the others are in redux)
*   Format: JSON
*   ReadBy: api-staging
*   WrittenBy: pipeline-staging, worker-staging
*   Resource: s3


## processed-matrix-production/[experiment_id]/r.rds



*   Description: processed matrix resulting from applying the pipeline.
*   Format: RDS
*   ReadBy: pipeline-production, worker-production
*   WrittenBy: pipeline-production
*   Resource: s3


## processed-matrix-staging/[sandbox_id-experiment_id]/r.rds



*   Description: processed matrix resulting from applying the pipeline.
*   Format: RDS
*   ReadBy: pipeline-staging, worker-staging
*   WrittenBy: pipeline-staging
*   Resource: s3


## worker-results-production/[?_id]



*   Description: worker responses too big to be placed in the SNS (instead keys to these S3 objects are placed in SNS)
*   Format: JSON
*   ReadBy: api-production 
*   WrittenBy: worker-production
*   Resource: s3


## worker-results-staging/[?_id]



*   Description: worker responses too big to be placed in the SNS (instead keys to these S3 objects are placed in SNS)
*   Format: JSON
*   ReadBy: api-staging
*   WrittenBy: worker-staging
*   Resource: s3


# DynamoDB


## experiments-production/[experiment_id]



*   Description: process config  data for the experiment
*   Format: JSON
*   PartitionKey: experimentId
*   ReadBy: worker-production
*   WrittenBy: data-ingest, data-upload-production, data-processing-production
*   Resource: dynamo


## experiments-staging/[sandbox_id-experiment_id]



*   Description: process config  data for the experiment
*   Format: JSON
*   PartitionKey: sandboxId-experimentId
*   ReadBy: worker-staging
*   WrittenBy: biomage-utils/stage, data-upload-staging, data-processing-staging
*   Resource: dynamo


## samples-production/[experiment_id]



*   Description: metadata regarding the experiment’s samples (like species, input files, input type, etc…)
*   Format: JSON
*   PartitionKey: experimentId
*   ReadBy: worker-production
*   WrittenBy: data-ingest, data-upload-production, data-processing-production
*   Resource: dynamo


## samples-staging/[sandbox_id-experiment_id]



*   Description: metadata regarding the experiment’s samples (like species, input files, input type, etc…)
*   Format: JSON
*   PartitionKey: sandboxId-experimentId
*   ReadBy: wor	ker-staging
*   WrittenBy: biomage-utils/stage, data-upload-staging, data-processing-staging
*   Resource: dynamo

 


## plots-tables-production/[experiment_id]



*   Description: metadata of the plots and tables
*   Format: JSON
*   PartitionKey: experimentId
*   SortKey: plotUuid
*   ReadBy: api-production
*   WrittenBy: api-production
*   Resource: dynamo


## plots-tables-staging/[sandbox_id-experiment_id]



*   Description: metadata of the plots and tables
*   Format: JSON
*   PartitionKey: sandboxId-experimentId
*   SortKey: plotUuid
*   ReadBy: api-staging
*   WrittenBy: api-staging
*   Resource: dynamo