import { createContext, useContext, useState } from "react";

const HomePageContext = createContext({});

export function HomeContext({ children }) {

  let HomeStateInit = {
    currentPage: 0,
    pageSize: 24
  }

  const [HomeState, setHomeState] = useState(HomeStateInit)
  const setStateVar = (field, value) => setHomeState({ ...HomeState, [field]: value })

  return (
    <HomePageContext.Provider value={{ ...HomeState, setStateVar }}>
      {children}
    </HomePageContext.Provider>
  )
}

export function useHomeContext() {
  return useContext(HomePageContext);
}