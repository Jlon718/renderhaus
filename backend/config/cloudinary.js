const cloudinary = require('cloudinary').v2;

// Configure Cloudinary
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
});

/**
 * Upload a 3D model file to Cloudinary
 * @param {Buffer} fileBuffer - The file buffer
 * @param {string} fileName - The original file name
 * @param {Object} options - Additional upload options
 * @returns {Promise} - Cloudinary upload result
 */
const uploadModel = async (fileBuffer, fileName, options = {}) => {
  try {
    console.log('Starting Cloudinary upload for:', fileName);
    
    // Determine folder based on file type
    let folder = 'renderhaus/models';
    if (options.metadata && options.metadata.type === 'thumbnail') {
      folder = 'renderhaus/thumbnails';
    }
    
    const result = await new Promise((resolve, reject) => {
      cloudinary.uploader.upload_stream(
        {
          resource_type: 'raw', // For non-image files like .gltf, .glb, .obj
          folder: folder,
          public_id: fileName.split('.')[0], // Use filename without extension as public_id
          use_filename: true,
          unique_filename: true, // Changed to true to avoid conflicts
          chunk_size: 6000000, // 6MB chunks for large files
          timeout: 300000, // 5 minutes timeout
        },
        (error, result) => {
          if (error) {
            reject(error);
          } else {
            resolve(result);
          }
        }
      ).end(fileBuffer);
    });

    console.log('Cloudinary upload successful:', {
      publicId: result.public_id,
      url: result.secure_url
    });

    // Return in the same format as uploadcare for compatibility
    return {
      fileId: result.public_id,
      cdnUrl: result.secure_url,
      originalUrl: result.url,
      fileName: fileName
    };
  } catch (error) {
    console.error('Cloudinary upload error:', error);
    throw new Error(`Cloudinary upload failed: ${error.message}`);
  }
};

/**
 * Delete a file from Cloudinary
 * @param {string} publicId - The public ID of the file to delete
 * @returns {Promise} - Cloudinary deletion result
 */
const deleteModel = async (publicId) => {
  try {
    return await cloudinary.uploader.destroy(publicId, {
      resource_type: 'raw'
    });
  } catch (error) {
    throw new Error(`Cloudinary deletion failed: ${error.message}`);
  }
};

module.exports = {
  cloudinary,
  uploadModel,
  deleteModel
};
