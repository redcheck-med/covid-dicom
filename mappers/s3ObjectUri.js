import {bucketName} from '../utils/constants.js';
export default src => {
  return `dicomweb://s3.amazonaws.com/${bucketName}/${src.Key}`;
}