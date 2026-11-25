import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
const origins = new Set(['https://www.calcite.yt','https://calcite.yt','https://calcite-dev.github.io']);
Deno.serve(async req => {
 const origin=req.headers.get('origin')||'';
 const headers={'Access-Control-Allow-Origin':origins.has(origin)?origin:'null','Access-Control-Allow-Headers':'authorization, x-client-info, apikey, content-type','Access-Control-Allow-Methods':'POST, OPTIONS','Vary':'Origin','Content-Type':'application/json'};
 const out=(data:unknown,status=200)=>new Response(JSON.stringify(data),{status,headers});
 if(!origins.has(origin))return out({error:'Origin not allowed'},403);
 if(req.method==='OPTIONS')return new Response(null,{headers});
 if(req.method!=='POST')return out({error:'Method not allowed'},405);
 try {
 const raw=await req.text();if(raw.length>24000)return out({error:'Too large'},413);
 const body=JSON.parse(raw);if(body.trap)return out({error:'Invalid submission'},400);
 const db=createClient(Deno.env.get('SUPABASE_URL')!,Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!,{auth:{persistSession:false}});
 const {data:id,error}=await db.rpc('record_contact',{answers:body.answers});if(error)return out({error:'Submission rejected'},400);
 let status='Not configured';
 const key=Deno.env.get('RESEND_API_KEY'),to=Deno.env.get('CONTACT_TO'),from=Deno.env.get('CONTACT_FROM');
 if(key&&to&&from){try{const res=await fetch('https://api.resend.com/emails',{method:'POST',headers:{Authorization:`Bearer ${key}`,'Content-Type':'application/json','Idempotency-Key':`calcite-contact-${id}`},body:JSON.stringify({from,to:[to],subject:'New Calcite contact message',text:body.answers.map((a:{label:string,answer:string})=>`${a.label}: ${a.answer}`).join('\n\n')}),signal:AbortSignal.timeout(10000)});status=res.ok?'Sent to provider':'Delivery failed'}catch{status='Delivery failed'}}
 await db.from('contact_messages').update({email_status:status}).eq('id',id);
 return out({saved:true});
 }catch{return out({error:'Unable to submit'},400)}
});
