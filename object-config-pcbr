#!/bin/bash
# Configuring OVHcloud Object Storage Lifecycle and Policies for Prism Central Backup and Recovery
# Preq. documented in Nutanix Support Portal https://portal.nutanix.com/page/documents/details?targetId=Prism-Central-Guide-vpc_7_5:mul-configuring-generic-s3-compliant-object-lifecycle-and-policies-t.html


BUCKET_NAME="ntnx-pcbr-yas"
ENDPOINT_URL="https://s3.rbx.io.cloud.ovh.net"
PROFILE="ovhcloud"

# Step 1: Create bucket with Object Lock enabled
echo "Creating bucket with Object Lock..."
aws s3api create-bucket \
  --bucket ${BUCKET_NAME} \
  --object-lock-enabled-for-bucket \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

# Step 2: Enable versioning (automatically enabled with Object Lock, but explicit is better)
echo "Enabling versioning..."
aws s3api put-bucket-versioning \
  --bucket ${BUCKET_NAME} \
  --versioning-configuration Status=Enabled \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

# Step 3: Configure Object Lock with 31-day retention (COMPLIANCE mode)
echo "Configuring Object Lock with 31-day retention..."
aws s3api put-object-lock-configuration \
  --bucket ${BUCKET_NAME} \
  --object-lock-configuration '{
    "ObjectLockEnabled": "Enabled",
    "Rule": {
      "DefaultRetention": {
        "Mode": "COMPLIANCE",
        "Days": 31
      }
    }
  }' \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

# Step 4: Configure lifecycle rules
echo "Configuring lifecycle rules..."
aws s3api put-bucket-lifecycle-configuration \
  --bucket ${BUCKET_NAME} \
  --lifecycle-configuration '{
    "Rules": [
      {
        "ID": "ExpireCurrentVersions",
        "Status": "Enabled",
        "Expiration": {
          "Days": 31
        },
        "Filter": {}
      },
      {
        "ID": "ExpireNoncurrentVersions",
        "Status": "Enabled",
        "NoncurrentVersionExpiration": {
          "NoncurrentDays": 1
        },
        "Filter": {}
      },
      {
        "ID": "DeleteExpiredDeleteMarkers",
        "Status": "Enabled",
        "Expiration": {
          "ExpiredObjectDeleteMarker": true
        },
        "Filter": {}
      },
      {
        "ID": "AbortIncompleteMultipartUpload",
        "Status": "Enabled",
        "AbortIncompleteMultipartUpload": {
          "DaysAfterInitiation": 1
        },
        "Filter": {}
      }
    ]
  }' \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

# Step 5: Verify configuration
echo ""
echo "=== Verifying Bucket Configuration ==="

echo ""
echo "Bucket Versioning Status:"
aws s3api get-bucket-versioning \
  --bucket ${BUCKET_NAME} \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

echo ""
echo "Object Lock Configuration:"
aws s3api get-object-lock-configuration \
  --bucket ${BUCKET_NAME} \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

echo ""
echo "Lifecycle Configuration:"
aws s3api get-bucket-lifecycle-configuration \
  --bucket ${BUCKET_NAME} \
  --endpoint-url ${ENDPOINT_URL} \
  --profile ${PROFILE}

echo ""
echo "Bucket creation and configuration completed successfully!"
