"use strict";
import { bucketName } from "../utils/constants.js";
import s3ObjectUri from "../mappers/s3ObjectUri.js";

export const listObjects = (folderId) => {
  var s3 = new AWS.S3();
  var params = {
    Bucket: bucketName,
    Prefix: folderId
  };

  return new Promise((resolve, reject) => {
    s3.makeUnauthenticatedRequest("listObjects", params, function(err, data) {
      if (err) {
        console.log(err);
        reject(err);
      } else {
        console.log(data);
        resolve(
          (data.Contents || []).filter((item, idx) => idx > 0).map(s3ObjectUri)
        );
      }
    });
  });
}
