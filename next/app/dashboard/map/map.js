"use client";
import React from 'react';
import { GoogleMap, useJsApiLoader, Rectangle } from '@react-google-maps/api';

/**
 * @typedef {{ lat: number, lng: number }} LatLng
 */

/**
 * @typedef {Object} MyMapComponentProps
 * @property {LatLng} center - The center coordinates for the map.
 * @property {google.maps.LatLngBounds|google.maps.LatLngBoundsLiteral|null} [bounds] - The area to outline.
 */

/**
 * @param {MyMapComponentProps} props
 * @returns {JSX.Element}
 */
export default function MyMapComponent({ center, bounds }) {
  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
  });

  if (!isLoaded) {
    return <div>Loading Map...</div>;
  }

  const containerStyle = {
    width: '100%',
    height: '100%'
  };

  // Options for outlining the area (a red border with no fill)
  const rectangleOptions = {
    strokeColor: "#FF0000",
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillOpacity: 0,
    clickable: false,
    draggable: false,
    editable: false,
    visible: true,
  };

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={12}
    />
  );
}
