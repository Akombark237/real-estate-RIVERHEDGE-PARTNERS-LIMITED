import { useEffect } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix for default marker icon
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

const PropertyMap = ({ latitude, longitude, title, address, height = '400px' }) => {
  // Default to Abuja, Nigeria if no coordinates provided
  const defaultLat = 9.0765
  const defaultLng = 7.3986
  
  const lat = latitude || defaultLat
  const lng = longitude || defaultLng
  const position = [lat, lng]

  return (
    <div style={{ height, width: '100%' }} className="rounded-xl overflow-hidden shadow-lg">
      <MapContainer
        center={position}
        zoom={latitude && longitude ? 15 : 12}
        style={{ height: '100%', width: '100%' }}
        scrollWheelZoom={false}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {latitude && longitude && (
          <Marker position={position}>
            <Popup>
              <div className="text-center">
                <p className="font-semibold">{title}</p>
                <p className="text-sm text-gray-600">{address}</p>
              </div>
            </Popup>
          </Marker>
        )}
      </MapContainer>
    </div>
  )
}

export default PropertyMap

