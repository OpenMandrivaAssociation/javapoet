Name:		javapoet
Version:	1.13.0
Release:	1
Summary:	Java API for generating Java source files
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/square/javapoet
Source0:	https://github.com/square/javapoet/archive/refs/tags/javapoet-%{version}.tar.gz#/javapoet-%{version}.tar.gz

BuildArch:	noarch
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	mvn(org.sonatype.oss:oss-parent:pom::)
BuildSystem:	maven
BuildOption(install):	--file-name javapoet

%description
JavaPoet generates .java source from a Java API. Gradle's instrumentation
processor uses it.

%prep
%autosetup -n javapoet-javapoet-%{version}
# The compiler plugin is pinned to Error Prone. That checker is not
# packaged, and plain javac compiles this tree.
python - <<'PY'
import xml.etree.ElementTree as ET

def local(tag):
    return tag.rsplit("}", 1)[-1]

tree = ET.parse("pom.xml")
root = tree.getroot()
for plugin in root.iter():
    if local(plugin.tag) != "plugin":
        continue
    artifact = next((c.text for c in plugin if local(c.tag) == "artifactId"), None)
    if artifact != "maven-compiler-plugin":
        continue
    for child in list(plugin):
        if local(child.tag) == "dependencies":
            plugin.remove(child)
        elif local(child.tag) == "configuration":
            for item in list(child):
                if local(item.tag) in {"compilerId", "forceJavacCompilerUse"}:
                    child.remove(item)
tree.write("pom.xml", xml_declaration=True, encoding="unicode")
PY

%files -f .mfiles
%doc LICENSE.txt README.md
