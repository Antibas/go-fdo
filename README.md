# FIDO Device Onboard - Go Library
## Instructions
1. Open 2 Terminals
2. On each terminal, run `./scripts/start_server.bash` & `./scripts/start_server_to0.bash`. Those two servers are the same, with the only difference that the second one has a Rendezvous server address. Normally I would have to manually switch between the two servers for each purpose. For the purpose of the demonstration, I start both servers simultaneously at the same time in different ports.
3. Run `python3 api.py`
4. Open FIDO Dashboard.
5. Initialize & start the client (device) with the DI URL.
6. For the RV registration, initialize the client (device) again, get the GUID and register it to the RV blob. Perform the client's TO1 only.
7. Verify key exchanges
8. Get the following:
      - The client's GUID.
      - A randomly generated public key.
9. Perform an ownership transfer using the previous credentials.
10. Obtain the ownership voucher.

## Issues
- [ ] Credential Reuse Protocol fix
## Next Steps
- [ ] Modify the IPs so that the client/server sides can run in separate devices