# Questions & Answers

## How to add a new webpage

1. Create a new file in the `routes` folder, for example `newpage.jsx`.

2. Add the following code to this file:

```jsx
import {createRoute} from "@tanstack/react-router";
import {rootRoute} from "./root";
import Navbar from "../components/Navbar.jsx";
import NewPage from "../components/NewPage.jsx";

export const newPageRoute = createRoute({
    getParentRoute: () => rootRoute,
    path: "/new",
    component: () => (
        <>
            <Component/>
        </>
    ),
});

```

3. To make sure the router recognizes the new route, you need to add it to the `routeTree` in your main routing file
   `root.jsx`"

```jsx
export const routeTree = rootRoute.addChildren([
    configRoute,
    overviewRoute,
    detailRoute,
    newPageRoute, // Add your new page route here
]);
```

## What does the API do  and where is it located

The API is located in the back-end of the project. Specifically, it is implemented in the `app.py` file. The API acts as
a communication layer between the frontend and the simulation.

## Which simulation framework is used and why

The simulation uses the Mesa framework. The justification for this choice can be found in the `Onderzoek Verschillende Sim Frameworks.pdf` file in the `docs` folder.