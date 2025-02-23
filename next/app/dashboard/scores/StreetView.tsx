import { useEffect, useRef } from "react";

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY; // Replace with your API Key

interface StreetViewProps {
  latlng: Array<number>,
  heading?: number;
  pitch?: number;
  zoom?: number;
}

const StreetView: React.FC<StreetViewProps> = ({ latlng, heading = 165, pitch = 0, zoom = 1 }) => {
  const streetViewRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const loadGoogleMaps = async () => {
      if (!window.google) {
        const script = document.createElement("script");
        script.src = `https://maps.googleapis.com/maps/api/js?key=${GOOGLE_MAPS_API_KEY}`;
        script.async = true;
        script.defer = true;
        script.onload = () => initStreetView();
        document.head.appendChild(script);
      } else {
        initStreetView();
      }
    };

    const initStreetView = () => {
      if (streetViewRef.current && window.google) {
        new google.maps.StreetViewPanorama(streetViewRef.current, {
          position: { lat: latlng[0], lng: latlng[1] },
          pov: { heading: 165, pitch: 0 },
          zoom: 1,
          fullscreenControl: false,
        });
      }
    };

    loadGoogleMaps();
  }, []);

  return <div ref={streetViewRef} style={{ width: "100%", height: "400px" }} />;
};


export default StreetView;