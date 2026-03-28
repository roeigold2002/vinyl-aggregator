import React from 'react'
import '../styles/components.css'

export const PriceComparison = ({ prices }) => {
  // Sort by price ascending
  const sortedPrices = [...prices].sort((a, b) => a.price_ils - b.price_ils)

  return (
    <div className="price-comparison">
      <h4>Price Comparison</h4>
      <table className="price-table">
        <thead>
          <tr>
            <th>Store</th>
            <th>Price</th>
            <th>Stock</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {sortedPrices.map((price, idx) => (
            <tr key={idx} className={idx === 0 ? 'best-price' : ''}>
              <td className="store-name">{price.store_name}</td>
              <td className="price">₪{price.price_ils.toFixed(2)}</td>
              <td className="stock">
                <span className={`stock-badge ${price.in_stock ? 'in-stock' : 'out-of-stock'}`}>
                  {price.in_stock ? 'In Stock' : 'Out of Stock'}
                </span>
              </td>
              <td className="action">
                <a 
                  href={price.store_url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="buy-button"
                >
                  Buy →
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default PriceComparison
