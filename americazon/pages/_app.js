import Home from '.';
import '../styles/globals.css'

import { QueryClient, QueryClientProvider } from "react-query";

import NextNProgress from "nextjs-progressbar";

function MyApp({ Component, pageProps }) {

  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <NextNProgress />
      <Component {...pageProps} />
    </QueryClientProvider>
  )
}

export default MyApp;
