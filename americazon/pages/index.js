import SearchBar from "../components/SearchBar";
import axios from "axios";

export default function Home({ departments }) {

  return (
    <div>
      <SearchBar departments={departments} />
    </div>
  )
}

export async function getStaticProps() {
  const res = await axios.get("http://localhost:3000/api/departments");
  let data = res.data;

  return {
    props : {
      departments : data,
    },
  }
}
