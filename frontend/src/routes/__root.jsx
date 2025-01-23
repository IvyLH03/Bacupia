import * as React from 'react'
import { Outlet, createRootRoute } from '@tanstack/react-router'
import { Typography } from '@mui/material'

export const Route = createRootRoute({
  component: RootComponent,
})

function RootComponent() {
  return (
    <React.Fragment>
      <Outlet />
      <br/>
      <footer>
        <Typography>&copy; 2025 IvyLH03</Typography>
      </footer>
    </React.Fragment>
  )
}
