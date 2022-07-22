export default async function fetchSearch( query ) {
    const res = await fetch(`/api/products/searchProducts?${(new URLSearchParams(query)).toString()}`);
    return res.json();
}