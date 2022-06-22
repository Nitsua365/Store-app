import axios from "axios";

export default async function fetchSearch( data ) {
    const res = await axios.get(`${process.env.LOCAL_API}/api/products/searchProducts`, { params: { ...data }});
    return res;
}