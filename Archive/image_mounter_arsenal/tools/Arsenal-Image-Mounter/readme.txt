Please read "Arsenal Recon - End User License Agreement.txt" carefully before using this software.

Arsenal Image Mounter
Many Windows®-based disk image mounting solutions mount the contents of disk images as shares or partitions, rather than complete (a/k/a “physical” or “real”) disks, which limits their usefulness to digital forensics practitioners and others. Arsenal Image Mounter mounts the contents of disk images as complete disks in Windows. As far as Windows is concerned, the contents of disk images mounted by Arsenal Image Mounter are real SCSI disks, allowing users to benefit from disk-specific features like integration with Disk Manager, launching virtual machines (and then bypassing Windows authentication), managing BitLocker-protected volumes, mounting Volume Shadow Copies, and more.

End Users: If Arsenal Image Mounter is run without a license, it will run in "Free Mode" and provide core functionality. If Arsenal Image Mounter is licensed, it will run in "Professional Mode” with full functionality enabled.

Feature highlights:
[Free Mode] Mount raw, forensic, and virtual machine disk images as complete (a/k/a “real”) disks on Windows
[Free Mode] Temporary write support with replayable delta files for all supported disk image formats
[Free Mode] Save "physically" mounted objects to various disk image formats
[Free Mode] Identify (with details), unlock, fully decrypt, and disable/suspend BitLocker-protected volumes
[Free Mode] Virtually mount optical images
[Free Mode] RAM disk creation with either static or dynamic memory allocation
[Free Mode] Command-line interface (CLI) executables
[Free Mode] MBR injection, fake disk signatures, removable disk emulation, and much more

[Professional Mode] Effortlessly launch virtual machines from disk images
[Professional Mode] Extremely powerful Windows authentication bypass within virtual machines
[Professional Mode] Volume Shadow Copy mounting (standard, with Windows NTFS driver bypass, or as complete disks)
[Professional Mode] Launch virtual machines directly from Volume Shadow Copies
[Professional Mode] Windows file system driver bypass (FAT, NTFS, ExFAT, HFS+, Ext2/3/4, etc.)
[Professional Mode] Exposure of NTFS metadata, slack, and unallocated in Windows file system driver bypass mode
[Professional Mode] Virtually mount archives and directories
[Professional Mode] Save disk images with fully-decrypted BitLocker volumes

Developers: Arsenal Image Mounter source code, APIs, and executables are available for royalty-free use in open source projects. Commercial projects (and other projects not licensed under an AGPL v3 compatible license) that would like to use Arsenal Image Mounter source code, APIs, and/or executables must contact Arsenal (sales@ArsenalRecon.com) to obtain alternative licensing.

Please Note: We recommend excluding/whitelisting Arsenal Image Mounter's folder and/or executables (ArsenalImageMounter.exe and aim_cli.exe) in your anti-virus software, as we have encountered situations in which anti-virus software has prevented (sometimes silently) Arsenal Image Mounter from launching successfully. When launching virtual machines with AIM, you may also need to instruct your anti-virus software to ignore/allow the "utilman.exe" threat.

Detailed feature descriptions (Mount options):
Read only disk device - Mount the disk image as a read-only disk device. No write operations will be allowed.

Write temporary disk device - Mount the disk image as a writable disk device. Modifications will be written to a write-overlay differencing file and the original disk image will not be changed. Sometimes referred to as write-overlay or write-copy mode. (Note - required for launching virtual machines.) If you would like to choose an alternate location for the differencing file, check the "Specify an alternate differential file location" box. AIM will also ask for an alternate differential file location if the disk image you are about to mount is already open one or more times in this mode, or if writing to the same location as the disk image is not possible because the location in which the disk image is located is write protected. If you would like AIM to delete the differencing file after the disk image is unmounted, check the "Delete differencing file after unmount" box. This option is disabled when the "Automatically remount at Arsenal Image Mounter startup" box is checked.

Write original disk device - Mount the disk image as a writable disk device. Modifications will be written to the disk image. (Caution - this option modifies the original disk image.)

Windows file system driver bypass - Mount the disk image as a virtual read-only file system, using DiscUtils rather than Windows file system drivers. This mount option is often used to bypass file system security and expose NTFS metafiles and streams. May also be useful to read files from disk images containing corrupted file systems. Please note, BitLocker-protected volumes are not supported and disk size values are an approximation of each volume's total file size (including things like multiple links to the same file and files with sparse allocation) so the size may appear larger than the expected volume size.

Sector size - Arsenal Image Mounter will normally select the correct sector size by default, based on disk image metadata, but there are situations in which it may need to be set manually. For example, you may need to set a sector size manually if the sector size is unusual and you are dealing with a raw disk image (without metadata) or the sector size specified in disk image metadata is incorrect. 

Fake disk signature - Report a random disk signature to Windows. Useful if the disk image contains a zeroed-out disk signature or you are attempting to mount a duplicate disk signature. (Note - requires a valid MBR and partition table. Not compatible with GPT partitions or images without a partition table.)

Create “removable” disk device - Emulate the attachment of a USB thumb drive, which may facilitate the successful mounting of disk images containing partitions rather than complete disks or disk images without partition tables. (Caution - see relevant FAQ for caveats.)

Automatically remount at Arsenal Image Mounter startup - Remount the disk image with the current mount options when AIM next starts. To retain this persistent mounting, simply quit AIM with the disk image mounted. To cancel this persistent mounting, use "Remove" or "Remove all" before quitting AIM.

Detailed feature descriptions (Main screen and dropdown menus):
Mount VSCs - Mount Volume Shadow Copies (VSCs) within a disk image (a list of VSCs is provided along with timestamps which allows any combination of VSCs to be mounted) with the following options:
•   Standard Volume Shadow Copy mount - Mount contents of VSCs using Windows NTFS driver. This option is fast, but does not expose file system metafiles and does not bypass file system security.
•   Volume Shadow Copy mount with Windows file system driver bypass - Mount contents of VSCs using DiscUtils NTFS driver. Useful to expose NTFS metafiles and to bypass file system security.
•   Write temporary Volume Shadow Copy mount - Mount contents of VSCs as complete disks in write-temporary mode using Windows NTFS driver. This option is useful for launching VSCs into virtual machines, but does not expose file system metafiles and does not bypass file system security.

Launch VM – Launch a Hyper-V virtual machine using the selected AIM-mounted disk. The disk image should be mounted in write temporary mode before using this feature, which is designed to make booting the contents of a disk image in a virtual machine more efficient, reliable, and useful than other methods. AIM will determine whether the disk image should be launched as a Generation 1 or Generation 2 virtual machine - see https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/plan/should-i-create-a-generation-1-or-2-virtual-machine-in-hyper-v for more details about the two Generations. The virtual machine is created with 2 CPUs, half of free host RAM (maximum of 4GB), two network adapters (not connected by default), one DVD-ROM (without any attached image) and the AIM-mounted disk as the primary IDE or SCSI HD. The Launch VM feature currently works (with full functionality) on Windows 8.1/10 (and Server 2012 R2/2016) x64 and requires that Hyper-V role be running on physical hardware, not within a virtual machine. Information from Microsoft about installing Hyper-V on Windows 10 is available at https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/quick-start/enable-hyper-v. Arsenal's preference in terms of installing Hyper-V is the "Enable Hyper-V with CMD and DISM" method. If you are unsure whether Hyper-V is running, the output from "sc query HvService" at a command prompt can be helpful.

Upon selecting Launch VM, AIM offers various options related to launching the virtual machine. You can choose to:
•   Configure the network connection so that it is disconnected (i.e. completely isolated), shared between VMs, shared between VMs and host, or set to the default switch with external NAT.
•   Enable guest services to provide copy/paste and other functionality between the VM and host. This is not recommended when isolation between the VM and host is preferred.
•   Check file systems and boot environment, repairing and adjusting as necessary. If this option is available (not greyed out), Arsenal recommends that you not deselect it.
•   Disable/suspend BitLocker-protected volumes, so that they do not need to be unlocked again once the VM is running.
•   Inject AIM Virtual Machine Tools and adjust boot drivers. Some disk images can be difficult to boot directly into virtual machines, so AIM can inject*1 a small application into virtual machines running Windows*2. AIM Virtual Machine Tools can display a list of accounts (accounts without tangible folder structure or without crucial Registry information are not listed in AIM Virtual Machine Tools, as there would effectively be nothing to login to and/or no way to do so) and can also open an administrative command prompt from the login screen. AIM Virtual Machine Tools will launch automatically on Windows XP and can be accessed via the “Ease of Access” icon on Windows Vista/7/8/8.1/10*3.
•   Boot with last Windows shutdown time (and disable Hyper-V's automatic time updates), which is useful (for example) to avoid time-based automatic cleanup functions (such as browser history cleanup) and to deal with time-based software licensing.
•   Bypass Windows authentication*4 using a variety of techniques, including policy adjustments, so that any password input will work. Local, Microsoft (cloud), Active Directory, and Azure Active Directory accounts, using many kinds of authentication including passwords, PINs, biometrics, images, and smart cards, are supported. Accounts will be provided with administrative privileges if requested or if the original privileges are unavailable. Please note that to access certain things in Windows like EFS-encrypted files and folders and cached login credentials you will need to crack, and not bypass, account authentication*5. Also - if you already have credentials for a Windows account, Arsenal recommends disabling this option so (for example) if you mistype a user's password you will be alerted to that fact rather than logged in anyway.
•   Bypass Data Protection API (DPAPI), which provides seamless access (particularly in concert with AIM's Windows authentication bypass) to the last logged-on user's DPAPI-protected content such as website, network share, and application credentials as well as files and folders protected by Encrypting File System (EFS). DPAPI-protected content is normally made available after a user successfully logs into Windows, but AIM's DPAPI bypass makes it available without having the user's credentials. This option will be available in certain situations when AIM first launches a Windows 10 x64 system with local or Microsoft (cloud) accounts into a virtual machine. Please note, this option currently works best with single-user systems and will not persist across reboots.
•   Start Windows kernel debugging with WinDbg.

*1 AIM will perform anti-virus evasion within the virtual machine to ensure that AIM Virtual Machine Tools runs properly.
*2 A file named "AIM_MODIFIED.txt" will be placed on the root of each Windows volume in which AIM Virtual Machine Tools has made adjustments. These adjustments are temporary by design, based on "Write temporary..." mounting.
*3 Depending on your anti-virus software and settings, you may need to exclude/whitelist AIM's folder and/or executables (ArsenalImageMounter.exe and aim_cli.exe) and/or temporarily disable real-time protection to ensure that AIM Virtual Machine Tools will be injected properly. You may also need to instruct your anti-virus software to ignore/allow the "utilman.exe" threat while the VM is booting.
*4 It is not always possible to identify an authoritative DOMAIN\USER combination for cached domain accounts in certain states, so AIM may create a DOMAIN\USER combination to facilitate access to those accounts. AIM Virtual Machine Tools will display AIM-created DOMAIN\USER combinations in red.
*5 In the case of Active Directory accounts, if a domain controller is available it is quite easy to set up a virtual network between it and the clients (all running in virtual machines launched by AIM), which will allow you to reset account passwords from the domain controller. Resetting passwords in this way will allow you access to previously inaccessible items on the clients such as cached login credentials and EFS-encrypted files and folders.

Additional notes regarding Launch VM:
•   AIM will create a RAM disk (which is quickly placed offline) when launching certain combinations of operating system, architecture, and partitioning into a VM. The RAM disk created by AIM is temporary, and used to make adjustments to the boot process in situations which include launching Windows 7 (or earlier) on a GPT disk into a VM.
•   If you would like to see whether your AIM-launched VMs are Generation 1 or Generation 2, open an administrative PowerShell and run "get-vm | format-list Name,Generation, State"

Mount archive file –  Select zip, cab, wim, and tar (raw or gzip or bzip2 compressed) files to mount read only with CD/DVD-ROM emulation or as a standard file system. If an archive file is mounted as a CD/DVD-ROM, it can be saved as an ISO image or attached directly to a virtual machine, but normal limitations apply such as a 4GB file size limit and a maximum path length of about 60 characters. If an archive file is mounted as a standard file system, there is no limitation on file size or path length, but it cannot be saved as an ISO image or attached directly to a virtual machine. Note that wim files often contain more than one image, so more than one virtual drive may appear. This feature is useful (for example) when you want to perform analysis of particular items within an archive in a read-only manner and/or do not want to extract anything from the archive to the file system.

Mount directory – Select a directory to mount as a read-only virtual CD/DVD-ROM. Includes “Boot image” option to create a bootable CD/DVD by injecting a boot image into the area reserved by the El-Torito standard. This option is sometimes used to boot operating system installation and repair tools (which exist loose in a directory as opposed to on a bootable CD/DVD or in a bootable ISO) into a virtual machine. By default, the "Boot image type" option is set to "NoEmulation" - in other words, it will be set to the typical (and modern) way to configure a boot image. The "Boot image type" option can be set to use floppy or hard disk emulation if desired. This feature is useful (for example) when you want to perform analysis of particular items within a directory in a read-only manner. Also facilitates the attachment of a directory to a virtual machine as if it is a virtual CD/DVD-ROM, which is useful when attaching a directory directly is not possible or you prefer to attach the directory read only.

Create new image file - Create and mount a new disk image file with an NTFS partition. Image formats supported are the same as the "Save as new image" file option. If a raw format is selected, it will be created with the sparse file attribute. This feature is useful (for example) when testing the behavior of digital forensics tools, file systems, and/or volume and disk encryption.

Save as new image file - Save a “physically” mounted object, including deltas, to a new raw (.raw, .dd, .img, .ima, .bin), virtual machine (.vhd, .vhdx, .vdi, .vmdk), or dmg (.dmg) disk image. This function can also be used to save virtually mounted objects (such as archives or directories mounted as CD/DVD-ROMs) as raw CD/DVD images, using the extensions .iso and .bin. Some users may leverage this feature to effectively convert from one disk image (or other source) format to another, but please note that (1) the source is saved as it currently appears to Windows - including (for example) injected MBRs and fake disk signatures (which can be applied to the current AIM session even when the disk image is mounted read only) as well as other deltas, and (2) some disk image formats (particularly virtual machine disk image formats) require unique GUIDs within their headers, so for effective hash value comparisons you will need to hash the contents of those disk images rather than the disk images themselves.

Show BitLocker status (all BitLocker-protected volumes) - Displays BitLocker protector IDs and types for all BitLocker-protected volumes within the currently selected disk. Also displays BitLocker recovery keys (numeric passwords) if the volumes are currently unlocked.

Unlock BitLocker-protected volumes - Unlocking BitLocker-protected volumes will decrypt their contents "on the fly" during the current Windows session. The BitLocker-protected data will still be stored encrypted on disk.

Fully decrypt BitLocker-protected volumes - Fully decrypting BitLocker-protected volumes will completely remove BitLocker, resulting in the previously BitLocker-protected data now being stored unencrypted on disk.

Disable/suspend BitLocker-protected volumes - Disabling (a/k/a suspending) BitLocker-protected volumes will disable their "protectors" (such as passwords) to allow seamless access to them. The BitLocker-protected data will still be stored encrypted on disk. Disabled BitLocker-protected volumes are sometimes referred to as being in "Clear Key Mode."

Save as fully decrypted image file - Saving BitLocker-protected volumes to a fully decrypted image file is an efficient way (saving time and disk space) to unlock BitLocker-protected volumes and create a new disk image with any previously BitLocker-protected volumes fully decrypted. Arsenal recommends mounting the BitLockered disk image read-only before using this feature.

Automatically start Arsenal Image Mounter at logon - Start AIM automatically during logon.

Attach to existing virtual machine - Attach a "physically" mounted object to a virtual machine launched by AIM. If you attach an AIM-mounted disk image, AIM-created RAM disk, or VHDX, you will be asked to place the object offline so that the virtual machine has exclusive access to it. If you attach a folder or archive mounted by AIM with CD/DVD-ROM emulation, you will not need to place the object offline as that concept is not relevant to CD/DVD-ROM emulation. Also, please note that CD/DVD-ROM emulation is inherently read only. 

Create RAM disk with fixed memory allocation - Create one or more RAM disks, with fixed memory allocation, as "real" disks containing NTFS file systems. These RAM disks can then be attached to virtual machines, saved to any of AIM's supported disk image formats, and more. RAM disks are sometimes used to meet extreme performance requirements (which HDDs or SSDs cannot) and to temporarily store sensitive files, because they are not written to the physical disk except during hibernation.

Create dynamically allocated RAM disk from VHD template - Create one or more RAM disks, with dynamic memory allocation (memory allocated as files are added to the RAM disk and deallocated when files are deleted), as "real" disks containing NTFS file systems. When using this feature, a VHD image file is selected as a "template" for the RAM disk. The contents of the VHD will be on the RAM disk when it is created, but the VHD will not be modified when the contents of the RAM disk change. These RAM disks can then be attached to virtual machines, saved to any of AIM's supported disk image formats, and more.

Rescan SCSI bus - Rescanning the SCSI bus may be useful if a disk image mounted by Arsenal Image Mounter does not appear in Windows, or if a dismounted disk image continues to appear there. This is a rarely used feature which is typically used only in debug scenarios involving compatibility issues with AIM and other drivers or applications causing unexpected behavior. The "Rescan Disks" option in Disk Management is similar in effect, except that it will rescan all storage buses instead of the AIM virtual SCSI adapter specifically.

FAQs:
Why is Arsenal Image Mounter different than other disk image mounting solutions?
Many disk image mounting solutions mount the contents of disk images in Windows as shares or partitions (rather than "complete" disks), which limits their usefulness. Arsenal Image Mounter is the first and only open source solution for mounting the contents of disk images as complete disks in Windows. We have also developed a significant amount of functionality that is particularly useful to the digital forensics and incident response community.

What are the requirements for running Arsenal Image Mounter?
Arsenal strongly recommends running Arsenal Image Mounter on Windows 10 (and Server 2016/2019) x64 so that all functionality (e.g. launching virtual machines and BitLocker-related functionality) works as intended. Most (i.e. not all!) of AIM's core functionality is available on Vista/7/8/8.1 and Server 2012/2012 R2 x64 if .NET 4.5 is installed. Most (i.e. not all!) of AIM's core functionality is available on both x64 and x86 versions of Vista/7/8/8.1 (and Server 2012/2012 R2 x64) when specifically using Arsenal Image Mounter CLI (if .NET 4.0 is installed) or Arsenal Image Mounter Low Level. Significant AIM functionality is unavailable in Windows versions prior to Vista - so while Arsenal Image Mounter CLI can be run on XP with .NET 4.0, and Arsenal Image Mounter Low Level can be run (theoretically) on 2000 onward, Arsenal does not support these older versions of Windows due to the loss of functionality.

How can I increase performance from disk images mounted by Arsenal Image Mounter?
Storing disk images on the fastest possible storage media is the most efficient way of increasing performance from disk images mounted by Arsenal Image Mounter. Here are benchmarks from launching a Windows 10 disk image (184GB in size, E01 format) into a virtual machine with AIM (all benchmark times are from clicking Launch VM through Windows logon and seeing a user’s Desktop), which demonstrate the drastic differences in performance between disk images stored on hard disk drives (HDDs) and solid-state drives (SSDs):
•   Mounted unlocked BitLockered disk image from internal HDD - 4-6 minutes 
•   Mounted unlocked BitLockered disk image from internal SSD - 2-3 minutes
•   Mounted fully decrypted BitLockered disk mage from internal HDD (full decryption took 40-45 minutes) - 3-4 minutes
•   Mounted fully decrypted BitLockered disk image from internal SSD (full decryption took 10-15 minutes) - 1 minute

What file systems does Arsenal Image Mounter support?
When mounting disk images using the "Read only...", "Write temporary...", and "Write original..." mount options, Arsenal Image Mounter essentially "hands off" the contents of disk images to Windows as if they were real SCSI disks, so the file system drivers currently installed on Windows will be used as necessary. Arsenal has used NTFS, FAT32, ReFS, exFAT, HFS+, UFS, and EXT3 file systems contained within AIM-mounted disks successfully when the appropriate file system drivers were installed. AIM also supports bypassing Windows file system drivers and using DiscUtils file system drivers via the "Windows file system driver bypass" mount option.

What disk image formats does Arsenal Image Mounter support?
•   Raw (dd)
•   Advanced Forensics Format 4 (AFF4) 
•   EnCase (E01 and Ex01) if libewf is available
•   Virtual Machine Disk Files (VHD, VDI, XVA, VMDK, OVA) and checkpoints (AVHD, AVHDX) if DiscUtils is available

What do you mean when you use the phrase "disk images?"
When we use the phrase "disk images" we are using it loosely, in the sense that we are referring to images containing complete disks or partitions, whether they are in raw, virtual machine, or forensic formats.

Why are some files and folders inaccessible to me after mounting a disk image with Arsenal Image Mounter?
Arsenal Image Mounter passes the contents of disk images to Windows as if they were complete disks when using the "Read only...", "Write temporary...", and "Write original..." mount options. Once AIM has passed the contents of disk images mounted in these modes to Windows, the file system drivers you currently have installed take over and caveats like difficulty accessing protected files and folders may apply.

What file systems does the Windows file system driver bypass mount option support?
•   FAT 12/16/32
•   NTFS
Experimental support for:
•   Btrfs
•   Ext2/3/4 (except with 64 bit header fields used by some of the latest Linux distributions)
•   ExFAT
•   HFS+ 
•   SquashFs
•   UDF
•   XFS

Can you describe some of the things exposed by the Windows file system driver bypass mount option?
•   NTFS metafiles (e.g. $MFT, $LogFile, $UsnJrnl)
•   NTFS Alternate Data Streams (ADS) as files suffixed with their stream names alongside the "normal" files they are associated with
•   NTFS streams in the [METADATA] folder at the root of each volume. You will find the entire volume's folder structure replicated here, and within each folder you will find the associated streams using the naming convention (STREAMNAME)..(STREAMTYPE). You can also find concatenated stream data for the entire volume at the root of the [METADATA] folder, using the naming convention [(STREAMNAME)]..[(STREAMTYPE)]. The streams currently exposed are $OBJECT_ID, $INDEX_ROOT, $INDEX_ALLOCATION, $EA, and $LOGGED_UTILITY_STREAM.
•   On NTFS file systems, deleted files which have not been completely overwritten will be displayed in the [DELETED] folder at the root of each volume. Filenames will be appended (unless none of their clusters have been reallocated, in which case they will remain as is) to identify what percentage of their clusters have not yet been reallocated. If you see "[0pct]" appended to a filename, that indicates a very small number of clusters were reallocated and the percentage has been rounded down to 0. Also, orphans will be displayed within folders using the naming convention MFT-(#)_SEQ-(#). This functionality is based on the DiscUtils project and is best described as "quick file and folder recovery." Please note that while browsing the contents of the [DELETED] folder you may encounter various kinds of corruption related to deleted files and folders (which will result in the error "The disk structure is corrupted and unreadable.") and that the contents of deleted files from SSDs (as opposed to HDDs) will often be empty.

Does Arsenal Image Mounter have command-line functionality?
Yes, please see readme_cli.txt for more details. In short, Arsenal Image Mounter CLI (aim_cli.exe) is a .NET 4.0 tool that provides most of Arsenal Image Mounter’s core functionality. The command “AIM_CLI /?” displays basic syntax for using Arsenal Image Mounter CLI. Arsenal Image Mounter CLI is provided with all versions of Arsenal Image Mounter. Arsenal Image Mounter Low Level (aim_ll.exe) is a tool that does not use .NET and provides more “low level” access to the Arsenal Image Mounter driver. The command “AIM_LL /?” displays basic syntax for using Arsenal Image Mounter Low Level. Arsenal Image Mounter Low Level is provided directly by Arsenal.

How can I share files, folders, and/or disks with virtual machines launched by Arsenal Image Mounter?
We normally prefer complete isolation of the virtual machines launched by AIM, but there are plenty of situations in which we need to share files, folders, and/or disks with virtual machines. Some methods of sharing include:
•    Enabling guest services in AIM's Launch VM options and then enabling Enhanced Session Mode (by selecting "Connect" at the "Display Configuration” dialog on Windows 8+) while the VM is booting, which will allow copy/paste between the host and virtual machine
•    Enabling guest services and Enhanced Session Mode as above will also allow USB drives already attached to the host to be attached to the VM, by selecting “Show Options/Local Resources/Local devices and resources/More…” at the Enhanced Session dialog, then under “Drives” selecting which USB drives to attach to the virtual machine
•    Using the Hyper-V Settings/SCSI Controller/Hard Drive/Add/Physical hard disk dropdown to add an offline disk to the VM once it has booted (a "disk" can be a real disk, a VHDX, or a RAM disk created by AIM), which will allow the disk to be used exclusively by the VM
•    In Generation 1 VMs, using the Hyper-V Settings/IDE Controller/Physical CD/DVD drive dropdown to add a directory or archive mounted by AIM with CD/DVD-ROM emulation to the VM once it has booted, which will allow the disk to be used simultaneously (but read only!) by the host and VM (if you have more than one directory or archive mounted by AIM and would like to switch between them in the VM, use the aforementioned Physical CD/DVD drive dropdown)
•    Using AIM's "Attach to existing virtual machine" feature which effectively replaces the "Hyper-V Settings/SCSI Controller" and "Hyper-V Settings/IDE Controller" methods mentioned above, to create more efficient workflow
•    Using PowerShell Direct (if both the host and virtual machine are running Windows 10 or Windows 2016) to run PowerShell commands such as Copy-Item and Enter-PSSession against a virtual machine, regardless of its network or remote management settings. Copy-Item is somewhat self explanatory and Enter-PSSession allows you to run commands within the virtual machine. See https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/powershell-direct for more information. Please note that PowerShell will ask for credentials of the account within the virtual machine that you are interested in, which you must provide as DOMAIN\USER or COMPUTER\USER. You do not need to enter a password if AIM has already performed Windows authentication bypass... but please note that even though you do not need to provide a password, PowerShell Direct still requires that the account originally had one. Here is sample syntax for Copy-Item first and then Enter-PSSession, each targeting a SANS Windows 10 workstation launched into a VM by AIM:
	Copy-Item -FromSession (New-PSSession -VMName AIM_base-rd01-cdrive.e01_5E3437D9) -Path “c:\users\tdungan\documents\demon core.pdf” -Destination c:\users\administrator\desktop
	Enter-PSSession -VMName AIM_base-rd01-cdrive.e01_5E3437D9

How can I or my organization contribute to Arsenal Image Mounter?
If Arsenal Image Mounter has become a valuable part of your toolkit, please let your colleagues in digital forensics know. We would also appreciate knowing how you use AIM and if you have any suggestions for future versions. If you or your organization have used AIM source code, APIs, and/or executables in open-source or commercial projects, please make sure you are complying with our licensing requirements. Commercial licensing of AIM source code, APIs, and/or executables helps us offset the cost of continued development, both in terms of Free and Professional Mode functionality.

What does "Create removable disk device" in the "Mount Options" screen do?
This function essentially emulates the attachment of a USB thumb drive. We have heard that it facilitates the mounting of disk images containing partitions rather than disks, even though Arsenal Image Mounter was initially designed to mount disks specifically. Characteristics (and limitations) of using this function include:
•    Windows (prior to Windows 10 Build 1703) will only identify and use the first partition in the disk image, even if it contains more than one partition
•    SAN policies such as requiring new devices to be mounted offline do not apply
•    Drive letters are always assigned even if automatic drive letter assignment is turned off
•    Windows identifies and uses file systems even for single-volume disk images that have no partition table
•    Inability to interact with Volume Shadow Copies natively

Do I need an Internet connection for Arsenal Image Mounter licensing?
You only need an Internet connection for Arsenal Image Mounter when you initially enter your license code and when you renew your license. If you cannot connect to the Internet, please see "How can I license Arsenal Image Mounter on an offline workstation?" below.

How can I license Arsenal Image Mounter on an offline workstation?
If you want your air-gapped workstation properly licensed for Arsenal Image Mounter, please:
1.) Open Arsenal Image Mounter and enter the license code you were given
2.) Upon realizing that no Internet connection is available, Arsenal Image Mounter will save a “.LIC” file to your ProgramData\ArsenalRecon folder
3.) On a workstation with Internet access, go to our Offline Activation page at https://www.softworkz.com/offline/offline.aspx and upload the “.LIC” file.
4.) Finally, copy the CDM file you receive to your ProgramData\ArsenalRecon folder
Your air-gapped workstation is now ready to run Arsenal Image Mounter!

How can I mount and launch virtual machines from disk images containing BitLocker-protected volumes?
When you use Arsenal Image Mounter to mount a disk image containing BitLocker-protected volumes, Windows will recognize those volumes and either ask to unlock them with a key (assuming they were in a locked state) or it will begin real-time decryption without requiring any user input (assuming they were in a disabled or suspended state.) There are a variety of ways in which "BitLockered disk images" (how Arsenal refers to disk images containing one or more BitLocker-protected volumes) can be launched into virtual machines. Here are some examples of workflows to launch BitLockered disk images into virtual machines:

This workflow is what we recommend if you would like maximum performance from the virtual machine:
1.) Use AIM to mount the disk image containing one or more BitLocker-protected volumes in write-temporary mode
2.) Use AIM's "Fully decrypt BitLocker-protected volumes" feature*
3.) Use AIM’s Launch VM feature to launch a virtual machine
4.) Run AIM Virtual Machine Tools by selecting the Ease of Access icon and use password bypass, etc. as desired

* This feature turns BitLocker off - fully decrypting all the contents of the BitLocker-protected volume. This is a time-consuming process and you can check on the status of full BitLocker decryption by using "manage-bde -status Volume Letter:" at a command prompt. Unlocking (rather than fully decrypting) BitLocker only results in real-time decryption of the BitLocker-protected volume contents as necessary, rather than full decryption.

This workflow is what we recommend for fastest access to the virtual machine (as there is no wait for full decryption):
1.) Use AIM to mount the disk image containing one or more BitLocker-protected volumes in write-temporary mode
2.) Use AIM's "Unlock BitLocker-protected volumes" feature or Windows itself on your forensic workstation to unlock the BitLocker-protected volume(s)
3.) Use AIM’s Launch VM feature to launch a virtual machine and select disable/suspend* BitLocker-protected volumes
4.) Run AIM Virtual Machine Tools by selecting the Ease of Access icon and use password bypass, etc. as desired

* By disable/suspend, we are referring to exposing the BitLockered volume's encryption key in the clear (the equivalent of "manage-bde -protectors -disable (Volume Letter:)"), turning off any volume protection. 

This workflow we do not recommend, because AIM Virtual Machine Tools will not be injected and you will be on your own in terms of logging in to any Windows accounts:
1.) Use AIM to mount the disk image containing one or more BitLockered-protected volumes in write-temporary mode
2.) Do not unlock BitLocker
3.) Use AIM’s Launch VM feature to launch a virtual machine (without allowing AIM to unlock and disable BitLocker protection)

Can I use Arsenal Image Mounter to mount Volume Shadow Copies (VSCs) in Windows natively?
Yes, you can enable Arsenal Image Mounter's “Professional Mode” to access VSC mounting functionality and choose to mount the contents of VSCs with either the Windows or DiscUtils NTFS drivers, or you can leverage AIM’s "Free Mode" image mounting functionality along with other tools such as Eric Zimmerman's VSCMount at https://ericzimmerman.github.io/#!index.md or as described on David Cowen’s blog at http://www.hecfblog.com/2014/02/daily-blog-240-arsenal-image-mounter.html.

How can I release or attach my mouse from a virtual machine launched by AIM?
You can release your mouse from Hyper-V by using the keyboard shortcut CTRL-ALT-LEFT ARROW. In some cases you may find that clicking within the Hyper-V virtual machine does not immediately attach your mouse, but if you wait until the operating system within the virtual machine is ready for input (in other words, it's not busy!) you will then be able to attach your mouse. More keyboard shortcuts can be found at https://blogs.msdn.microsoft.com/virtual_pc_guy/2008/01/14/virtual-machine-connection-key-combinations-with-hyper-v.

Can I use Arsenal Image Mounter to decrypt full-disk or volume encryption within disk images?
Yes, Arsenal Image Mounter is used frequently for this purpose. Generally speaking, you have two great options - use AIM to mount your disk image as a “real” disk and let full-disk or volume encryption software on your host proceed, or launch your disk image into a virtual machine to interact with either the full-disk encryption's limited OS or the volume encryption's native applications within the virtual machine. You can see screenshots from both of these options applied to a disk image containing Symantec Encryption Desktop (a/k/a PGP Desktop) at https://twitter.com/ArsenalRecon/status/1242094213929537540. If you are dealing with BitLocker, AIM also has BitLocker-related functionality to assist you.

Are you having trouble booting decrypted BitLocker volumes?
See Adam Bridge’s excellent blog post on modifying an NTFS volume’s Volume Boot Record (VBR) using Arsenal Image Mounter’s “Write temporary” mode at https://www.contextis.com/resources/blog/making-ntfs-volume-mountable-tinkering-vbr/.

How can I fix AIM’s drop-down menus from flying out beyond the GUI’s borders?
This behavior may be related to Windows Presentation Framework and “handedness.” Your handedness setting can be found by hitting Windows key+R, then pasting in “shell:::{80F3F1D5-FECA-45F3-BC32-752C152E456E}”. If your handedness setting is “Right-handed” you may want to change it to “Left-handed”.

Will using Hyper-V's "Enhanced Session Mode" cause any problems with Windows virtual machines?
Potentially, yes. We do not recommend using Hyper-V's Enhanced Session Mode (which appears as a "Display Configuration” dialog during the launch of virtual machines running Windows 8+ and essentially uses Remote Desktop to connect to the virtual machine) because unexpected policy issues may surface - for example, accounts may be prohibited from remote and password-less logons. If you are booting a virtual machine and see the Enhanced Session Mode dialog asking about screen resolution, just exit that dialog and you will be returned to direct console mode.

Why isn't Hyper-V running properly on bare metal even though I'm sure it's installed?
If you are sure Hyper-V has been installed, but when you run "sc query HvService" from a command prompt you are notified that it is not running, it's possible that there is an issue with boot configuration due to the presence of other virtualization platforms like VMware or Oracle VM VirtualBox. You may be able to resolve this issue by running "bcdedit /set hypervisorlaunchtype auto" at an administrative command prompt (which will result in Hyper-V starting at boot), but please note that you may need to reverse this action ("bcdedit /set hypervisorlaunchtype off") later to make sure your other virtualization platforms work as expected. 

Is it possible to deploy Arsenal Image Mounter unattended?
To some extent, yes. We can provide customers with an installation package containing the Arsenal Image Mounter driver and the AIM CLI application, which can be installed silently depending on circumstances. While the installation will be silent in terms of Arsenal Image Mounter itself, it may not be silent in terms of Windows due to policy - for example, users may need to confirm that they trust drivers from Arsenal.

Is there an Application Programming Interface (API)?
Yes – Arsenal Image Mounter provides both .NET and non-.NET APIs. You can find these APIs on our GitHub page at https://github.com/ArsenalRecon/Arsenal-Image-Mounter/tree/master/API.

What programming languages have been used to build Arsenal Image Mounter?
Arsenal Image Mounter’s Storport miniport driver is written in C and its user mode API library is written in VB.NET, which facilitates easy integration with .NET 4.0 applications.

Where can I find the source code?
Arsenal Image Mounter source code can be found on GitHub at https://github.com/ArsenalRecon/Arsenal-Image-Mounter.

How can I uninstall Arsenal Image Mounter?
If you would like to completely uninstall Arsenal Image Mounter (perhaps you want to revert to an earlier version), go to Device Manager\Storage controllers\Arsenal Image Mounter, right-click and select "Uninstall device". Then, from an administrative command prompt:
1.) [Optional] If you have the Windows Driver Kit (WDK) installed (or Visual Studio, or the Windows SDK), you can run "devcon remove *phdskmnt" (e.g. C:\Program Files (x86)\Windows Kits\10\Tools\x64\devcon remove *phdskmnt) instead of using Device Manager
2.) sc delete phdskmnt
3.) sc delete aimwrfltr
4.) [Optional] sc stop vhdaccess
5.) [Optional] sc delete vhdaccess
6.) [Optional] sc stop awealloc
7.) [Optional] sc delete awealloc
8.) [Optional] sc stop dokan1
9.) [Optional] sc delete dokan1
10.) Delete phdskmnt.sys and aimwrfltr.sys from C:\Windows\system32\drivers
11.) [Optional] Delete vhdaccess.sys, awealloc.sys and dokan1.sys from C:\Windows\system32\drivers
12.) Delete the Arsenal Image Mounter executables, libraries, and documentation from where you placed them

Clarifications regarding terminology:
The phrases "Removing disk" and "Unmounting disk image" essentially refer to the same thing when you see them in dialog boxes, documentation, and blog posts related to Arsenal Image Mounter.

Use and License
We chose a dual-license for Arsenal Image Mounter (more specifically, Arsenal Image Mounter’s source code, APIs, and executables) to allow for royalty-free use in open source projects, but require financial support from commercial projects.

Arsenal Consulting, Inc. (d/b/a Arsenal Recon) retains the copyright to Arsenal Image Mounter, including the Arsenal Image Mounter source code, APIs, and executables, being made available under terms of the Affero General Public License v3. Arsenal Image Mounter source code, APIs, and executables may be used in projects that are licensed so as to be compatible with AGPL v3. If your project is not licensed under an AGPL v3 compatible license and you would like to use Arsenal Image Mounter source code, APIs, and/or executables, contact us (sales@ArsenalRecon.com) to obtain alternative licensing.

Contributors to Arsenal Image Mounter must sign the Arsenal Contributor Agreement (“ACA”). The ACA gives Arsenal and the contributor joint copyright interests in the source code.

