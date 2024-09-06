@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the event loop for the session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    logging.info(f"Created event loop: {loop}")
    yield loop
    loop.close()
    logging.info(f"Closed event loop: {loop}")


@pytest.fixture(scope="session")
async def session(event_loop):
    """Create a new async session for tests, bound to the event loop."""
    async with async_engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    async with async_session_test() as session:
        logging.info(f"Session using event loop: {asyncio.get_event_loop()}")
        yield session
    async with async_engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
async def client(session):
    """Override the FastAPI dependency and set up an async test client."""

    async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
        logging.info(f"Override session using event loop: {asyncio.get_event_loop()}")
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        logging.info(f"Client using event loop: {asyncio.get_event_loop()}")
        yield ac
