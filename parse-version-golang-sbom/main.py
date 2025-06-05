import logging

from packageurl import PackageURL

logger = logging.getLogger("test")

sbom_map = {"github.com/containerd/containerd": "v1.6.18"}

sbom_name_to_purl = {"github.com/containerd/containerd": "pkg:golang/github.com/containerd/containerd@v1.6.18"}


def sbom_checker(package_name: str):
    "use this tool to check the version of the software package from the SBOM"
    "returns the software version if the package is present in the SBOM"
    "if the package is not in the SBOM returns False"

    try:
        version = sbom_map.get(package_name.lower().strip(),
                               check_if_golang(package_name.lower().strip(),
                                               sbom_map, sbom_name_to_purl))
    except Exception as e:
        logger.warning("Couldn't get version for package_name=%s, error details => " + str(e), package_name)
        version = False
    return version


def check_if_golang(package_name: str, sbom_map: dict[str, str], names_to_purls: dict[str, str]):
    """use this function only if not found package. In Golang, package name sometimes contains, in addition
    to the name itself, repository + namespace, and sometimes major version suffix.
    So in such case if the sbompackage' purl is of golang  then return the version also if the package_name
    is a substring of SBOMPackage' name or namespace/name
    returns the software version if the package is present in the SBOM
    "if the package is not in the SBOM returns False"

    Parameters
    ----------
     :param package_name: str
        A string representing the input package name which for it we're getting its version

     :param sbom_map:  dict[str, str]
        A dict representing the sbom packages, with each package name mapped to its version

     :param names_to_purls: dict[str, str]
        A dict representing the sbom packags, with each package name mapped to its full package URL.

      """
    for package, version in sbom_map.items():
        purl_string = names_to_purls.get(package)
        if "pkg:golang" in purl_string and package_name_matches(package_name, purl_string):
            return version

    return False


def package_name_matches(package_name, purl_string) -> bool:
    purl_object = PackageURL.from_string(purl_string)
    namespace_plus_name = purl_object.namespace + '/' + purl_object.name
    return (package_name == purl_object.name or (package_name == namespace_plus_name) or
            (package_name in namespace_plus_name))


sbom_checker("containerd")
