export async function Fetch({
    url,
    method = 'POST',
    args = {}
  }) {
    let str = JSON.stringify(args);

    if (method == 'GET') str = undefined;
  
    try {
      let res = await fetch(
        process.env.REACT_APP_API_URL + url,
        {
          method: method,
          body: str,
          headers: {
              'Content-Type': 'application/json',
          },
          referrer: "",
          credentials: 'include',
        }
      );
      json = await res.json();
  
      if (!res.ok) {
        throw Error(res.statusText);
      }
  
      if (json.status == "error") {
        throw Error(json.error);
      }
    } catch (err) {
      return Promise.reject(err);
    }
  
    return json;
  }
  