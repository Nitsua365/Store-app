import Home from '.';
import '../styles/globals.css'

import { QueryClient, QueryClientProvider } from "react-query";

import NextNProgress from "nextjs-progressbar";
import { HomeContext } from 'context/HomeContext';

import Layout from 'components/layouts';

export default function MyApp({ Component, pageProps }) {

  const queryClient = new QueryClient()

  return (
    <QueryClientProvider client={queryClient}>
      <NextNProgress />
      <HomeContext> 
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </HomeContext>
    </QueryClientProvider>
  )
}