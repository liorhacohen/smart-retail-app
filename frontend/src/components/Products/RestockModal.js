import React, { useState } from 'react';
import { X, Package, Plus } from 'lucide-react';
import { apiService } from '../../services/api';
import toast from 'react-hot-toast';
import './RestockModal.css';

const RestockModal = ({ product, onClose, onSuccess }) => {
  const [quantity, setQuantity] = useState('');
  const [reason, setReason] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!quantity || parseInt(quantity) <= 0) {
      toast.error('Please enter a valid quantity');
      return;
    }

    try {
      setLoading(true);
      
      await apiService.restockProduct(product.id, {
        quantity: parseInt(quantity),
        reason: reason || 'Manual restock'
      });
      
      toast.success(`Successfully restocked ${product.name}`);
      onSuccess();
    } catch (error) {
      toast.error('Failed to restock product');
    } finally {
      setLoading(false);
    }
  };

  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  const handleOverlayKeyDown = (e) => {
    if (e.key === 'Escape') {
      onClose();
    }
  };

  return (
    <div 
      className="modal-overlay" 
      onClick={handleOverlayClick}
      onKeyDown={handleOverlayKeyDown}
      role="button"
      tabIndex={0}
      aria-label="Close modal"
    >
      <div className="modal-content">
        <div className="modal-header">
          <h2>Restock Product</h2>
          <button className="modal-close" onClick={onClose}>
            <X size={20} />
          </button>
        </div>

        <div className="modal-body">
          <div className="product-info">
            <div className="product-icon">
              <Package size={24} />
            </div>
            <div>
              <h3>{product.name}</h3>
              <p>Current Stock: {product.quantity} units</p>
              <p>Minimum Level: {product.min_stock_level} units</p>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="restock-form">
            <div className="form-group">
              <label htmlFor="quantity">Quantity to Add</label>
              <input
                type="number"
                id="quantity"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="Enter quantity"
                min="1"
                required
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="reason">Reason (Optional)</label>
              <select
                id="reason"
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                className="form-select"
              >
                <option value="">Select reason</option>
                <option value="New shipment">New shipment</option>
                <option value="Manual restock">Manual restock</option>
                <option value="Return from customer">Return from customer</option>
                <option value="Found inventory">Found inventory</option>
                <option value="Correction">Inventory correction</option>
              </select>
            </div>

            {quantity && (
              <div className="restock-preview">
                <h4>After Restock:</h4>
                <p>New Stock Level: <strong>{product.quantity + parseInt(quantity || 0)} units</strong></p>
              </div>
            )}

            <div className="modal-actions">
              <button
                type="button"
                onClick={onClose}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  'Processing...'
                ) : (
                  <>
                    <Plus size={16} />
                    Restock Product
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RestockModal;