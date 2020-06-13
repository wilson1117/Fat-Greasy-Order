import { serve } from "https://deno.land/std@0.50.0/http/server.ts";
import { MongoClient } from "https://deno.land/x/mongo@v0.8.0/mod.ts";

const client = new MongoClient();
client.connectWithUri("mongodb://localhost:27017");
const db = client.database("order");
const list = db.collection("orderList");
const s = serve({ port: 8000 });

console.log("http://localhost:8000/");
console.log(await list.find({}));
for await (const req of s) {
    req.respond({ body: `${list}` });
}
