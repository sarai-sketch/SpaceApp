import {Canvas} from '@react-three/fiber';
import {OrbitControls, Float} from '@react-three/drei';
import {useMemo} from 'react';
import type {Crop} from '../rotation';
import * as THREE from 'three';
function Sprout({x,z,crop}:{x:number;z:number;crop:Crop}){
 const color=crop==='maiz'?'#54a943':crop==='papa'?'#70b65e':crop==='haba'?'#3fbf80':crop==='quinua'?'#bc77a4':'#79c5a4';
 const height=crop==='maiz'?.72:crop==='quinua'?.65:crop==='haba'?.5:.38;
 return <group position={[x,0,z]}>
 <mesh position={[0,height/2,0]} castShadow><cylinderGeometry args={[.025,.035,height,6]}/><meshStandardMaterial color="#45873d"/></mesh>
 {[-1,1].map((s,i)=><mesh key={i} position={[s*.12,height*.65+i*.03,0]} rotation={[0,0,s*.45]} castShadow><sphereGeometry args={[.20,.06,.10,8,6]}/><meshStandardMaterial color={color} side={THREE.DoubleSide}/></mesh>)}
 {crop==='maiz'&&<mesh position={[0,height*.78,0]}><sphereGeometry args={[.085,.16,.085,8,8]}/><meshStandardMaterial color="#ffd34c"/></mesh>}
 {crop==='quinua'&&<mesh position={[0,height+.06,0]}><sphereGeometry args={[.13,.19,.13,8,8]}/><meshStandardMaterial color="#db9bba"/></mesh>}
 {crop==='papa'&&<mesh position={[0,.17,0]}><sphereGeometry args={[.13,.1,.13,8,8]}/><meshStandardMaterial color="#91c65c"/></mesh>}
 </group>
}
function Plot({crop,x,z,selected,onClick}:{crop:Crop;x:number;z:number;selected:boolean;onClick:()=>void}){
 const plants=useMemo(()=>Array.from({length:20},(_,i)=>({x:-1.16+(i%5)*.58,z:-.76+Math.floor(i/5)*.52})),[]);
 return <group position={[x,0,z]} onClick={(e)=>{e.stopPropagation();onClick()}}>
 <mesh position={[0,.07,0]} receiveShadow><boxGeometry args={[3.15,.26,2.45]}/><meshStandardMaterial color={selected?'#bb874d':'#94603c'}/></mesh>
 <mesh position={[0,.19,0]} receiveShadow><boxGeometry args={[2.91,.06,2.22]}/><meshStandardMaterial color={crop==='descanso'?'#699f4e':'#78472c'}/></mesh>
 {plants.map((v,i)=><Sprout key={i} {...v} crop={crop}/>)}
 {selected&&<mesh position={[0,.02,0]}><boxGeometry args={[3.33,.07,2.63]}/><meshStandardMaterial color="#ffe275" emissive="#e5a32b" emissiveIntensity={.35}/></mesh>}
 </group>
}
function Tree({x,z}:{x:number;z:number}){return <group position={[x,0,z]}><mesh position={[0,.48,0]} castShadow><cylinderGeometry args={[.12,.19,.95,8]}/><meshStandardMaterial color="#94643d"/></mesh><mesh position={[0,1.25,0]} castShadow><sphereGeometry args={[.65,12,10]}/><meshStandardMaterial color="#71bd58"/></mesh><mesh position={[.34,1.43,.13]} castShadow><sphereGeometry args={[.38,10,8]}/><meshStandardMaterial color="#8ed56b"/></mesh></group>}
function Farm({rotation,season,selected,onSelect,widthMeters,lengthMeters}:{rotation:Crop[];season:number;selected:number;onSelect:(i:number)=>void;widthMeters:number;lengthMeters:number}){
 const crops=rotation;
 return <><color attach="background" args={['#b9eaff']}/><ambientLight intensity={1.5}/><hemisphereLight args={['#e4f8ff','#8eae65',1.6]}/><directionalLight position={[8,14,8]} intensity={2.2} castShadow shadow-mapSize={[1024,1024]}/>
 <mesh rotation={[-Math.PI/2,0,0]} position={[0,-.5,0]} receiveShadow><planeGeometry args={[200,200]}/><meshStandardMaterial color="#a9d886"/></mesh>
 <mesh position={[0,-.15,0]} receiveShadow><boxGeometry args={[widthMeters/10,.65,lengthMeters/10]}/><meshStandardMaterial color="#8dcb69"/></mesh>
 <mesh position={[0,-.47,0]}><boxGeometry args={[widthMeters/10+.2,.14,lengthMeters/10+.2]}/><meshStandardMaterial color="#ad8251"/></mesh>
 {[-3.35,0,3.35].map((x,i)=><Plot key={i} crop={crops[i]} x={x} z={0} selected={selected===i} onClick={()=>onSelect(i)}/>)}
 {[-4.8,4.8].map((x,i)=><Tree key={i} x={x} z={-3.15}/>)}
 {[-4.7,4.7].map((x,i)=><Tree key={'b'+i} x={x} z={3.3}/>)}
 <mesh position={[0,.04,2.25]}><boxGeometry args={[9.8,.08,.7]}/><meshStandardMaterial color="#e4c48b"/></mesh>
 <Float speed={1.5} rotationIntensity={0} floatIntensity={.15}><group position={[-4.9,1.7,1.8]}><mesh><sphereGeometry args={[.38,16,12]}/><meshStandardMaterial color="#f9f6ed"/></mesh><mesh position={[0,0,.31]}><sphereGeometry args={[.25,.19,.10,12,10]}/><meshStandardMaterial color="#8bd0e9"/></mesh><mesh position={[0,-.54,0]}><cylinderGeometry args={[.24,.34,.65,12]}/><meshStandardMaterial color="#f8f8f4"/></mesh></group></Float>
 </>
}
export default function Parcela3D({rotation,season,selected,onSelect,widthMeters=100,lengthMeters=100}:{rotation:Crop[];season:number;selected:number;onSelect:(i:number)=>void;widthMeters?:number;lengthMeters?:number}){
 return <div className="game-scene"><Canvas shadows camera={{position:[10,10,13],fov:39}} gl={{antialias:true}}><Farm rotation={rotation} season={season} selected={selected} onSelect={onSelect} widthMeters={widthMeters} lengthMeters={lengthMeters}/><OrbitControls enablePan={false} minDistance={9} maxDistance={24} maxPolarAngle={Math.PI/2.3} target={[0,.2,0]}/></Canvas><div className="scene-tip">👆 Toca una parcela para elegirla · Arrastra para girar</div></div>
}
