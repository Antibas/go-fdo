# FIDO Device Onboard - Go Library
## Instructions
1. Open 2 Terminals
2. On each terminal, run `./scripts/start_server.bash` & `./scripts/start_server_to0.bash`. Normally I would have to manually switch between the two servers for each purpose. For the purpose of the demonstration, I start both servers simultaneously at the same time in different ports, but the second server has as a TO0 the first's URL.
3. Open FIDO Dashboard.
4. Initialize & start the client (device) with the DI URL.
5. For the RV registration, initialize the client (device) again, get the GUID and register it to the RV blob. Perform the client's TO1 only.
6. Verify key exchanges
7. Get the following:
      - The client's GUID.
      - A randomly generated public key.
8. Perform an ownership transfer voucher using the previous credentials.
9. Obtain the ownership voucher.

## Issues
- [ ] Credential Reuse Protocol fix
## Next Steps
- [ ] Modify the IPs so that the client/server sides can run in separate devices