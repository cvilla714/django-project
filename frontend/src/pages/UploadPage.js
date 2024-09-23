import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';

const UPLOAD_IMAGE = gql`
  mutation UploadImage($image: String!) {
    uploadImage(image: $image) {
      success
      imageUrl
    }
  }
`;

const UploadPage = () => {
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null); // State for preview
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null); // New state to hold the uploaded image URL
  const [uploadImage] = useMutation(UPLOAD_IMAGE);

  // Handle file input change and set preview
  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setImage(file);

    // Set up preview URL
    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  // Handle the form submit (upload)
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      alert('Please select an image to upload');
      return;
    }

    // Convert image to base64 and send it to the server
    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

      try {
        const response = await uploadImage({ variables: { image: base64String } });
        console.log(response.data);

        // If upload is successful, set the uploaded image URL
        if (response.data.uploadImage.success) {
          setUploadedImageUrl(response.data.uploadImage.imageUrl);
        }
      } catch (error) {
        console.error('Error uploading image', error);
      }
    };

    reader.readAsDataURL(image);
  };

  return (
    <div>
      <h1>Upload Image</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleImageChange} />
        <br />
        {imagePreview && <img src={imagePreview} alt="Preview" width="200" />}
        <br />
        <button type="submit">Upload</button>
      </form>

      {/* Show a preview message while waiting for the image to be uploaded */}
      {imagePreview && <p>Previewing image before upload...</p>}

      {/* Show the uploaded image URL once the upload is successful */}
      {uploadedImageUrl && (
        <div>
          <h2>Image Uploaded Successfully!</h2>
          <p>Uploaded Image URL:</p>
          <a href={uploadedImageUrl} target="_blank" rel="noopener noreferrer">
            {uploadedImageUrl}
          </a>
          <br />
          <img src={uploadedImageUrl} alt="Uploaded" width="200" />
        </div>
      )}
    </div>
  );
};

export default UploadPage;
