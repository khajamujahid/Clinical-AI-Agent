'use client'
import { Canvas, useLoader } from '@react-three/fiber'
import { Float, OrbitControls, Environment } from '@react-three/drei'
import * as THREE from 'three'

function HolographicPortrait() {
  // This maps your 2D image onto a 3D floating plane
  const texture = useLoader(THREE.TextureLoader, '/nurse.jpg')
  return (
    <mesh>
      <planeGeometry args={[3, 4.5]} />
      <meshBasicMaterial map={texture} side={THREE.DoubleSide} />
    </mesh>
  )
}

export default function NurseScene() {
  return (
    <div className="relative h-full w-full">
      <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
        <ambientLight intensity={1.5} />
        <Float speed={2} rotationIntensity={0.2} floatIntensity={0.6}>
          <HolographicPortrait />
        </Float>
        <OrbitControls enableZoom={false} maxPolarAngle={Math.PI / 2 + 0.2} minPolarAngle={Math.PI / 2 - 0.2} />
      </Canvas>
    </div>
  )
}