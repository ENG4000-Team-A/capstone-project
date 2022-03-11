// import dependencies
import React from "react";

// import API mocking utilities from Mock Service Worker
import { rest } from "msw";
import { setupServer } from "msw/node";

// import react-testing methods
import { render, fireEvent, waitFor, screen } from "@testing-library/react";

// add custom jest matchers from jest-dom
import "@testing-library/jest-dom";

// component to test
import MachineCard from "../MachineCard";

const server = setupServer(
  rest.get("/timer", (req, res, ctx) => {
    // respond using a mocked JSON body
    return res(
      ctx.json({
        data: [
          {
            id: 1,
            name: "Machine #1",
            active: true,
            ip: "127.0.0.1",
            machine_type: "PS5",
          },
          {
            id: 2,
            name: "Machine #2",
            active: false,
            ip: "127.0.0.2",
            machine_type: "xbox",
          },
          {
            id: 3,
            name: "Machine #3",
            active: false,
            ip: "127.0.0.3",
            machine_type: "PS5",
          },
          {
            id: 4,
            name: "Machine #4",
            active: false,
            ip: "127.0.0.5",
            machine_type: "PS5",
          },
          {
            id: 5,
            name: "Machine #5",
            active: false,
            ip: "127.0.0.10",
            machine_type: "PS5",
          },
          {
            id: 6,
            name: "Machine #6",
            active: true,
            ip: "127.0.0.11",
            machine_type: "PS5",
          },
        ],
      })
    );
  })
);

// establish API mocking before all tests
beforeAll(() => server.listen());

// reset any request handlers that are declared as a part of our tests
// (i.e. for testing one-time error scenarios)
afterEach(() => server.resetHandlers());

// clean up once the tests are done
afterAll(() => server.close());

// Appears to have a router problem at the moment. Will address it soon.

test("render a card", async() => {
  render(<MachineCard />);

  // does this object truely exist?
  const isRendered = screen.getByTestId('machine_card');
  expect(isRendered)

})



