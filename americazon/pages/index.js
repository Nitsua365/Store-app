import { QueryClient, QueryClientProvider } from "react-query";

import SearchBar from "components/SearchBar";

import axios from "axios";

const queryClient = new QueryClient();

export default function Home({ departments }) {

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <div>
          <SearchBar departments={departments} />
        </div>
      </QueryClientProvider>
    </>
  )
}

export async function getStaticProps() {
  const res = await axios.get("http://localhost:3000/api/departments");

  return {
    props : {
      departments : res.data,
    },
  }
}
