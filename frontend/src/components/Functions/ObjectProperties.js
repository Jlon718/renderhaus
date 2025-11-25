import React from 'react';
import ColorPicker from './ColorPicker';
import './css/ObjectProperties.css';

const ObjectProperties = ({ 
  selectedObject, 
  onColorChange, 
  onAIColorSuggestion,
  onColorReset,
  onObjectDelete,
  onPositionChange,
  onObjectTransform
}) => {
  
  const handleDeleteObject = () => {
    if (onObjectDelete && selectedObject) {
      onObjectDelete(selectedObject.id);
    }
  };

  const handleColorReset = () => {
    if (onColorReset && selectedObject) {
      onColorReset(selectedObject.id);
    }
  };

  const handlePositionChange = (axis, value) => {
    if (onPositionChange && selectedObject) {
      onPositionChange(selectedObject.id, axis, value);
    }
  };

  const handleScaleChange = (value) => {
    if (onObjectTransform && selectedObject) {
      const scaleValue = [parseFloat(value), parseFloat(value), parseFloat(value)];
      onObjectTransform(selectedObject.id, 'scale', scaleValue);
    }
  };

  const handleRotationChange = (value) => {
    if (onObjectTransform && selectedObject) {
      const rotationValue = [0, parseFloat(value), 0];
      onObjectTransform(selectedObject.id, 'rotation', rotationValue);
    }
  };

  if (!selectedObject) {
    return (
      <div className="object-properties">
        <div className="no-selection-message">
          <div className="no-selection-icon">📦</div>
          <h3>No Object Selected</h3>
          <p>Click on a 3D object in the scene to view and edit its properties</p>
        </div>
      </div>
    );
  }

  return (
    <div className="object-properties">
      <div className="properties-header">
        <h2>Object Properties</h2>
        <button 
          className="delete-object-btn"
          onClick={handleDeleteObject}
          title="Delete Object"
        >
          🗑️
        </button>
      </div>

      <div className="object-info">
        <h3>{selectedObject.name}</h3>
        <p className="object-category">{selectedObject.category}</p>
      </div>

      {/* Position Section */}
      <div className="property-section">
        <h3 className="section-title">Position</h3>
        <div className="position-controls">
          {/* Y-axis (Height) */}
          <div className="position-control">
            <label>
              <span className="axis-label">Y (Height)</span>
              <span className="axis-value">{selectedObject.position?.[1]?.toFixed(2) || '0.00'}</span>
            </label>
            <div className="control-input-group">
              <input
                type="range"
                min="-2"
                max="5"
                step="0.1"
                value={selectedObject.position?.[1] || 0}
                onChange={(e) => handlePositionChange('y', e.target.value)}
                className="position-slider"
              />
              <input
                type="number"
                min="-2"
                max="5"
                step="0.1"
                value={selectedObject.position?.[1] || 0}
                onChange={(e) => handlePositionChange('y', e.target.value)}
                className="position-input"
              />
            </div>
          </div>

          {/* X-axis (Left/Right) */}
          <div className="position-control">
            <label>
              <span className="axis-label">X (Left/Right)</span>
              <span className="axis-value">{selectedObject.position?.[0]?.toFixed(2) || '0.00'}</span>
            </label>
            <div className="control-input-group">
              <input
                type="range"
                min="-10"
                max="10"
                step="0.1"
                value={selectedObject.position?.[0] || 0}
                onChange={(e) => handlePositionChange('x', e.target.value)}
                className="position-slider"
              />
              <input
                type="number"
                min="-10"
                max="10"
                step="0.1"
                value={selectedObject.position?.[0] || 0}
                onChange={(e) => handlePositionChange('x', e.target.value)}
                className="position-input"
              />
            </div>
          </div>

          {/* Z-axis (Forward/Backward) */}
          <div className="position-control">
            <label>
              <span className="axis-label">Z (Forward/Back)</span>
              <span className="axis-value">{selectedObject.position?.[2]?.toFixed(2) || '0.00'}</span>
            </label>
            <div className="control-input-group">
              <input
                type="range"
                min="-10"
                max="10"
                step="0.1"
                value={selectedObject.position?.[2] || 0}
                onChange={(e) => handlePositionChange('z', e.target.value)}
                className="position-slider"
              />
              <input
                type="number"
                min="-10"
                max="10"
                step="0.1"
                value={selectedObject.position?.[2] || 0}
                onChange={(e) => handlePositionChange('z', e.target.value)}
                className="position-input"
              />
            </div>
          </div>
        </div>
      </div>

      {/* Scale Section */}
      <div className="property-section">
        <h3 className="section-title">Scale (Size)</h3>
        <div className="scale-control-group">
          <label>
            <span className="axis-label">Uniform Scale</span>
            <span className="axis-value">{((selectedObject.scale?.[0] || 1) * 100).toFixed(0)}%</span>
          </label>
          <div className="control-input-group">
            <input
              type="range"
              min="0.1"
              max="3"
              step="0.1"
              value={selectedObject.scale?.[0] || 1}
              onChange={(e) => handleScaleChange(e.target.value)}
              className="position-slider"
            />
            <input
              type="number"
              min="0.1"
              max="3"
              step="0.1"
              value={selectedObject.scale?.[0] || 1}
              onChange={(e) => handleScaleChange(e.target.value)}
              className="position-input"
            />
          </div>
        </div>
      </div>

      {/* Rotation Section */}
      <div className="property-section">
        <h3 className="section-title">Rotation</h3>
        <div className="rotation-control-group">
          <label>
            <span className="axis-label">Y-axis (Yaw)</span>
            <span className="axis-value">{Math.round(((selectedObject.rotation?.[1] || 0) * 180) / Math.PI)}°</span>
          </label>
          <div className="control-input-group">
            <input
              type="range"
              min="0"
              max={Math.PI * 2}
              step="0.1"
              value={selectedObject.rotation?.[1] || 0}
              onChange={(e) => handleRotationChange(e.target.value)}
              className="position-slider"
            />
            <input
              type="number"
              min="0"
              max="360"
              step="1"
              value={Math.round(((selectedObject.rotation?.[1] || 0) * 180) / Math.PI)}
              onChange={(e) => handleRotationChange((parseFloat(e.target.value) * Math.PI) / 180)}
              className="position-input"
            />
          </div>
        </div>
      </div>

      {/* Color Section */}
      <div className="property-section">
        <ColorPicker
          selectedObject={selectedObject}
          onColorChange={onColorChange}
          onAIColorSuggestion={onAIColorSuggestion}
        />
        
        {/* Reset Color Button */}
        <div className="color-actions">
          <button 
            className="reset-color-btn"
            onClick={handleColorReset}
            title="Reset to original color"
          >
            🔄 Reset Color
          </button>
        </div>
      </div>
    </div>
  );
};

export default ObjectProperties;
