import React from 'react';
import { MapContainer, TileLayer, Marker, Tooltip, useMap } from 'react-leaflet';
import L from 'leaflet';
import redIconUrl from '../../assets/icons/marker.svg';
import yellowIconUrl from '../../assets/icons/marker (1).svg';

import styles from './MapMarkers.module.css';

interface PointData {
  id: number;
  lat: number;
  lng: number;
  color: 'red' | 'yellow';
  label?: string;
  address: string;
  deviation: number;
  riskLevel: 'high' | 'medium';
  checks: number;
  consumption?: { week: number; consumption: number }[]; // индивидуальные данные
  normalAverage?: number; // линия нормы
}


interface MapWithMarkersProps {
  points: PointData[];
  center?: [number, number];
  zoom?: number;
  activePointId?: string | number | null;
  onPointClick?: (point: PointData) => void;
}

// Иконки
const redIcon = L.icon({
  iconUrl: redIconUrl,
  iconSize: [24, 24],
  iconAnchor: [12, 12],
});

const yellowIcon = L.icon({
  iconUrl: yellowIconUrl,
  iconSize: [24, 24],
  iconAnchor: [12, 12],
});

// Отдельный компонент маркера с логикой перемещения карты
const SmartMarker: React.FC<{
  point: PointData;
  icon: L.Icon;
  onClick?: (point: PointData) => void;
}> = ({ point, icon, onClick }) => {
  const map = useMap();

  const handleClick = () => {
    map.flyTo([point.lat, point.lng], map.getZoom(), {
      duration: 0.8, // плавность
    });
    onClick?.(point);
  };

  return (
    <Marker
      position={[point.lat, point.lng]}
      icon={icon}
      eventHandlers={{ click: handleClick }}
    >
      {point.label && <Tooltip>{point.label}</Tooltip>}
    </Marker>
  );
};

export const MapMarkers: React.FC<MapWithMarkersProps> = ({
  points,
  center = [45.035, 38.976],
  zoom = 12,
  activePointId,
  onPointClick,
}) => {
  const filteredPoints = activePointId
    ? points.filter((p) => p.id === activePointId)
    : points;

  return (
    <MapContainer
      center={center}
      zoom={zoom}
      className={styles.mapCont}
      attributionControl={false}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution=""
      />
      {filteredPoints.map((point) => (
        <SmartMarker
          key={point.id}
          point={point}
          icon={point.color === 'red' ? redIcon : yellowIcon}
          onClick={onPointClick}
        />
      ))}
    </MapContainer>
  );
};
