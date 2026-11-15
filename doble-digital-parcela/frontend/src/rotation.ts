export type Crop = 'maiz'|'papa'|'haba'|'quinua'|'descanso';
export type Rotation = [Crop,Crop,Crop];
export const cropInfo:Record<Crop,{name:string;emoji:string;color:string;group:string;description:string}>={
 maiz:{name:'Maíz',emoji:'🌽',color:'#f5c951',group:'cereal',description:'Cereal que consume nutrientes'},
 papa:{name:'Papa',emoji:'🥔',color:'#ce976b',group:'tuberculo',description:'Tubérculo de gran importancia local'},
 haba:{name:'Haba',emoji:'🫛',color:'#76c66d',group:'leguminosa',description:'Leguminosa que puede contribuir al nitrógeno del suelo'},
 quinua:{name:'Quinua',emoji:'🌾',color:'#d99bca',group:'pseudocereal',description:'Cultivo andino; necesita manejo adaptado al lugar'},
 descanso:{name:'Cobertura',emoji:'🌿',color:'#69cda3',group:'cobertura',description:'Cobertura vegetal, no dejar suelo desnudo'}
};
export const crops=Object.keys(cropInfo) as Crop[];
export const starter:Rotation[]=[['maiz','haba','papa'],['papa','quinua','haba'],['maiz','descanso','quinua']];
export type RotationScore={soil:number;water:number;diversity:number;score:number;notes:string[]};
export function evaluate(rotation:Rotation):RotationScore{
 const groups=rotation.map(c=>cropInfo[c].group);
 const changes=groups.slice(1).filter((g,i)=>g!==groups[i]).length;
 const unique=new Set(groups).size;
 const legumes=rotation.filter(c=>c==='haba').length;
 const covers=rotation.filter(c=>c==='descanso').length;
 const repeat=rotation.slice(1).filter((c,i)=>c===rotation[i]).length;
 const soil=Math.min(100,Math.max(10,42+changes*13+legumes*13+covers*14-repeat*18));
 const water=Math.min(100,Math.max(10,48+changes*8+covers*18+legumes*5-repeat*10));
 const diversity=Math.round(unique/3*100);
 const score=Math.round(soil*.45+water*.25+diversity*.30);
 const notes:string[]=[];
 if(repeat)notes.push('Repetir el mismo cultivo seguido puede aumentar riesgos sanitarios y agotar recursos.');
 if(legumes)notes.push('Incluyes haba: una leguminosa que puede aportar beneficios al sistema.');
 if(covers)notes.push('Incluyes cobertura vegetal para proteger el suelo.');
 if(changes===2)notes.push('Cambias de familia o función entre temporadas.');
 if(!notes.length)notes.push('Prueba introducir una leguminosa o cobertura.');
 return {soil,water,diversity,score,notes};
}
