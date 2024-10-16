# FIDO Device Onboard - Go Library & Dashboard
## Introduction
The FIDO Device Onboard (FDO) process enables secure, automated onboarding of IoT devices through a series of well-defined steps and protocols. This library follows the [FIDO Device Onboard (FDO) Specification 1.1](https://fidoalliance.org/specs/FDO/FIDO-Device-Onboard-PS-v1.1-20220419/FIDO-Device-Onboard-PS-v1.1-20220419.html), which allows secure device provisioning by permitting "late binding" of device credentials, enabling a single manufactured device to onboard without modification to multiple IoT platforms.

The process goes as follows:

1. **Device Initialization:** The device is initialized with FDO credentials: A key pair is installed at first and the first entry in an *Ownership Voucher* - a digital document used throughout the device’s life to securely transfer ownership - is created based on that.
2. **Transfer Ownership Protocol 0 (TO0):** The new owner registers with a *Rendezvous Server (RV)*, an intermediate between the device and the owner storing important information for both of them. The owner provides the device’s *Globally Unique Identifier (GUID)* and other network metadata to the *RV*, allowing the device to locate the owner.
3. **Transfer Ownership Protocol 1 (TO1):** Powering up the device for the first time makes it invoke the *RV* using the previous *GUID* to obtain the owner's information. The device is then directed to the correct owner’s Onboarding Service.
4. **Transfer Ownership Protocol 2 (TO2):** The device and owner exchange credentials: The owner provides a valid *Ownership Voucher*, and the device, after it validates the owner’s credentials, replaces its old ones with them.
5. **Device Operation:** The device can now be managed by the new owner freely. This protocol is no longer needed unless the device's ownership changes.
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