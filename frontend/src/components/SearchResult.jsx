import { useSearchParams } from 'react-router-dom';

function SearchResult() {
  const [searchParams, setSearchParams] = useSearchParams();
  const token = searchParams.get('token');

  return <>{token}</>;
}

export default SearchResult;
