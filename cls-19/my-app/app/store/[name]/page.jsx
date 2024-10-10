import React from 'react'

export default function page({params,searchParams}) {
    // console.log(params.name,searchParams.q);
  return (
    <pre>    params are:{params.name} and searchParams are :
     {Object.keys(searchParams) +
      ` = `+Object.values(searchParams)}</pre>
  )
}
