import React, { useState } from 'react';
import { useMutation, gql } from '@apollo/client';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for redirection
import './UploadPage.css'; // Import the CSS for styling

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
  const [imagePreview, setImagePreview] = useState(null); // For the image preview
  const [uploadedImageUrl, setUploadedImageUrl] = useState(null);
  const [uploadImage] = useMutation(UPLOAD_IMAGE);
  const navigate = useNavigate(); // Use useNavigate hook for redirection

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    setImage(file);

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result); // Set the preview URL
    };
    if (file) {
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!image) {
      alert('Please select an image to upload');
      return;
    }

    const reader = new FileReader();
    reader.onloadend = async () => {
      const base64String = reader.result.replace('data:', '').replace(/^.+,/, '');

      try {
        const response = await uploadImage({ variables: { image: base64String } });
        setUploadedImageUrl(response.data.uploadImage.imageUrl);
        setImagePreview(null); // Clear preview after upload
        setImage(null); // Clear selected image
      } catch (error) {
        console.error('Error uploading image', error);
      }
    };

    reader.readAsDataURL(image);
  };

  const handleSignOut = () => {
    // Clear local storage or cookies
    localStorage.removeItem('authToken'); // Adjust depending on where your JWT is stored
    // Redirect to login
    navigate('/'); // Use navigate to redirect the user to the login page
  };

  return (
    <div className="upload-page">
      <div className="upload-container">
        <h2>Upload an Image</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" accept="image/*" onChange={handleImageChange} />

          {/* Image preview section */}
          {imagePreview && (
            <div className="image-preview-container">
              <img src={imagePreview} alt="Preview" className="image-preview" />
            </div>
          )}

          {uploadedImageUrl ? (
            <p className="uploaded-message">
              Image uploaded successfully!
              <br />
              <a href={uploadedImageUrl} target="_blank" rel="noopener noreferrer">
                {uploadedImageUrl}
              </a>
            </p>
          ) : (
            <div>
              <button type="submit" className="upload-button">
                Upload Image
              </button>
            </div>
          )}
        </form>
        <button className="sign-out-button" onClick={handleSignOut}>
          Sign Out
        </button>
      </div>
    </div>
  );
};

export default UploadPage;
