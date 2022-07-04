import withQuery from "with-query";


export default async function fetchSearch( query ) {
    const res = await fetch(withQuery(`/api/products/searchProducts`, { searchString : query.searchString }));
    return res.json();
}