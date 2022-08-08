export default async function fetchDepartment() {
    const res = await fetch(`/api/departments`);
    return res.json();
}