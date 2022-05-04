import SearchBar from "../components/SearchBar";
import axios from "axios";

export default function Home({ departments }) {
  return (
    <div className="self-center">
      <SearchBar departments={departments} />
    </div>
  )
}

export async function getStaticProps() {
  const res = await axios.get("http://localhost:3000/api/departments/getAllDepartments");
  const departments = res.data.map(e => e.name);

  return {
    props : {
      departments,
    },
  }
}
