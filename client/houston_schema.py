import sgqlc.types
import sgqlc.types.datetime

houston_schema = sgqlc.types.Schema()


__docformat__ = "markdown"


########################################################################
# Scalars and Enumerations
########################################################################
Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime


class DeploymentStatusType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `UNKNOWN`None
    * `DEPLOYING`None
    * `UNHEALTHY`None
    * `HEALTHY`None
    """

    __schema__ = houston_schema
    __choices__ = ("UNKNOWN", "DEPLOYING", "UNHEALTHY", "HEALTHY")


class EntityType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `WORKSPACE`None
    * `DEPLOYMENT`None
    * `SYSTEM`None
    """

    __schema__ = houston_schema
    __choices__ = ("WORKSPACE", "DEPLOYMENT", "SYSTEM")


class ExecutorType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `LocalExecutor`None
    * `CeleryExecutor`None
    * `KubernetesExecutor`None
    """

    __schema__ = houston_schema
    __choices__ = ("LocalExecutor", "CeleryExecutor", "KubernetesExecutor")


Float = sgqlc.types.Float

ID = sgqlc.types.ID


class Id(sgqlc.types.Scalar):
    __schema__ = houston_schema


Int = sgqlc.types.Int


class JSON(sgqlc.types.Scalar):
    __schema__ = houston_schema


class MetricType(sgqlc.types.Enum):
    """Enumeration Choices:

    * `DEPLOYMENT_STATUS`None
    * `DEPLOYMENT_TASKS`None
    * `DEPLOYMENT_DATABASE`None
    * `DEPLOYMENT_SCHEDULER`None
    * `DEPLOYMENT_QUOTAS`None
    * `DEPLOYMENT_USAGE`None
    """

    __schema__ = houston_schema
    __choices__ = (
        "DEPLOYMENT_STATUS",
        "DEPLOYMENT_TASKS",
        "DEPLOYMENT_DATABASE",
        "DEPLOYMENT_SCHEDULER",
        "DEPLOYMENT_QUOTAS",
        "DEPLOYMENT_USAGE",
    )


class Operator(sgqlc.types.Enum):
    """Enumeration Choices:

    * `AND`None
    * `OR`None
    """

    __schema__ = houston_schema
    __choices__ = ("AND", "OR")


class Role(sgqlc.types.Enum):
    """Enumeration Choices:

    * `SYSTEM_ADMIN`None
    * `SYSTEM_EDITOR`None
    * `SYSTEM_VIEWER`None
    * `WORKSPACE_ADMIN`None
    * `WORKSPACE_EDITOR`None
    * `WORKSPACE_VIEWER`None
    * `DEPLOYMENT_ADMIN`None
    * `DEPLOYMENT_EDITOR`None
    * `DEPLOYMENT_VIEWER`None
    * `USER`None
    """

    __schema__ = houston_schema
    __choices__ = (
        "SYSTEM_ADMIN",
        "SYSTEM_EDITOR",
        "SYSTEM_VIEWER",
        "WORKSPACE_ADMIN",
        "WORKSPACE_EDITOR",
        "WORKSPACE_VIEWER",
        "DEPLOYMENT_ADMIN",
        "DEPLOYMENT_EDITOR",
        "DEPLOYMENT_VIEWER",
        "USER",
    )


String = sgqlc.types.String


class Uuid(sgqlc.types.Scalar):
    __schema__ = houston_schema


########################################################################
# Input Objects
########################################################################
class AirflowReleaseWhereUniqueInput(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("id", "tag")
    id = sgqlc.types.Field(String, graphql_name="id")

    tag = sgqlc.types.Field(String, graphql_name="tag")


class DeploymentRoles(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("deployment_id", "role")
    deployment_id = sgqlc.types.Field(Id, graphql_name="deploymentId")

    role = sgqlc.types.Field(Role, graphql_name="role")


class DeploymentWhereUniqueInput(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("id", "release_name")
    id = sgqlc.types.Field(String, graphql_name="id")

    release_name = sgqlc.types.Field(String, graphql_name="releaseName")


class EmailWhereUniqueInput(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("id", "address", "token")
    id = sgqlc.types.Field(String, graphql_name="id")

    address = sgqlc.types.Field(String, graphql_name="address")

    token = sgqlc.types.Field(String, graphql_name="token")


class InputEnvironmentVariable(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("key", "value", "is_secret")
    key = sgqlc.types.Field(String, graphql_name="key")

    value = sgqlc.types.Field(String, graphql_name="value")

    is_secret = sgqlc.types.Field(Boolean, graphql_name="isSecret")


class InviteSearch(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("invite_uuid", "email")
    invite_uuid = sgqlc.types.Field(Uuid, graphql_name="inviteUuid")

    email = sgqlc.types.Field(String, graphql_name="email")


class Limits(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("cpu", "memory")
    cpu = sgqlc.types.Field(Int, graphql_name="cpu")

    memory = sgqlc.types.Field(Int, graphql_name="memory")


class Requests(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("cpu", "memory")
    cpu = sgqlc.types.Field(Int, graphql_name="cpu")

    memory = sgqlc.types.Field(Int, graphql_name="memory")


class Resources(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("requests", "limits")
    requests = sgqlc.types.Field(Requests, graphql_name="requests")

    limits = sgqlc.types.Field(Limits, graphql_name="limits")


class RoleBindingWhereUniqueInput(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(String, graphql_name="id")


class Scheduler(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("replicas", "resources")
    replicas = sgqlc.types.Field(Int, graphql_name="replicas")

    resources = sgqlc.types.Field(Resources, graphql_name="resources")


class UserSearch(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = (
        "user_id",
        "user_uuid",
        "username",
        "email",
        "full_name",
        "created_at",
        "updated_at",
    )
    user_id = sgqlc.types.Field(Id, graphql_name="userId")

    user_uuid = sgqlc.types.Field(Uuid, graphql_name="userUuid")

    username = sgqlc.types.Field(String, graphql_name="username")

    email = sgqlc.types.Field(String, graphql_name="email")

    full_name = sgqlc.types.Field(String, graphql_name="fullName")

    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class Webserver(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("resources", "use_default_airflow_image")
    resources = sgqlc.types.Field(Resources, graphql_name="resources")

    use_default_airflow_image = sgqlc.types.Field(
        Boolean, graphql_name="useDefaultAirflowImage"
    )


class Workers(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("replicas", "termination_grace_period_seconds", "resources")
    replicas = sgqlc.types.Field(Int, graphql_name="replicas")

    termination_grace_period_seconds = sgqlc.types.Field(
        Int, graphql_name="terminationGracePeriodSeconds"
    )

    resources = sgqlc.types.Field(Resources, graphql_name="resources")


class WorkspaceWhereUniqueInput(sgqlc.types.Input):
    __schema__ = houston_schema
    __field_names__ = ("id",)
    id = sgqlc.types.Field(String, graphql_name="id")


########################################################################
# Output Objects and Interfaces
########################################################################
class AirflowImage(sgqlc.types.Type):
    """The `AirflowImage` compound type represents a valid Airflow
    version and Docker Tag in Astronomer.
    """

    __schema__ = houston_schema
    __field_names__ = ("version", "channel", "tag")
    version = sgqlc.types.Field(String, graphql_name="version")

    channel = sgqlc.types.Field(String, graphql_name="channel")

    tag = sgqlc.types.Field(String, graphql_name="tag")


class AirflowRelease(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "tag",
        "version",
        "url",
        "level",
        "description",
        "release_date",
        "channel",
    )
    tag = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="tag")

    version = sgqlc.types.Field(String, graphql_name="version")

    url = sgqlc.types.Field(String, graphql_name="url")

    level = sgqlc.types.Field(String, graphql_name="level")

    description = sgqlc.types.Field(String, graphql_name="description")

    release_date = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="releaseDate"
    )

    channel = sgqlc.types.Field(String, graphql_name="channel")


class AppConfig(sgqlc.types.Type):
    """The `AppConfig` compound type exposes some basic platform-level
    configuration.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "version",
        "base_domain",
        "smtp_configured",
        "manual_release_names",
        "prometheus_enabled",
        "elastic_search_enabled",
    )
    version = sgqlc.types.Field(String, graphql_name="version")
    """The version of the platform that is running."""

    base_domain = sgqlc.types.Field(String, graphql_name="baseDomain")
    """The base domain that the platform is running at."""

    smtp_configured = sgqlc.types.Field(Boolean, graphql_name="smtpConfigured")
    """Is SMTP configured properly? This determines if the platform is
    able to send emails.
    """

    manual_release_names = sgqlc.types.Field(Boolean, graphql_name="manualReleaseNames")
    """Can users specify their own release names for deployments?"""

    prometheus_enabled = sgqlc.types.Field(Boolean, graphql_name="prometheusEnabled")
    """Is Prometheus (metrics) enabled?"""

    elastic_search_enabled = sgqlc.types.Field(
        Boolean, graphql_name="elasticSearchEnabled"
    )
    """Is ElasticSearch (logs) enabled?"""


class AstroUnit(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "cpu",
        "memory",
        "pods",
        "airflow_conns",
        "actual_conns",
        "price",
    )
    cpu = sgqlc.types.Field(Int, graphql_name="cpu")

    memory = sgqlc.types.Field(Int, graphql_name="memory")

    pods = sgqlc.types.Field(Float, graphql_name="pods")

    airflow_conns = sgqlc.types.Field(Float, graphql_name="airflowConns")

    actual_conns = sgqlc.types.Field(Float, graphql_name="actualConns")

    price = sgqlc.types.Field(Float, graphql_name="price")


class AuthConfig(sgqlc.types.Type):
    """The `AuthConfig` compound type contains information about how the
    authentication system is configured. This is primarily used to
    display the Astronomer login page according to current system
    configuration.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "public_signup",
        "external_signup_url",
        "initial_signup",
        "local_enabled",
        "providers",
    )
    public_signup = sgqlc.types.Field(Boolean, graphql_name="publicSignup")

    external_signup_url = sgqlc.types.Field(String, graphql_name="externalSignupUrl")

    initial_signup = sgqlc.types.Field(Boolean, graphql_name="initialSignup")

    local_enabled = sgqlc.types.Field(Boolean, graphql_name="localEnabled")

    providers = sgqlc.types.Field(
        sgqlc.types.list_of("AuthProvider"), graphql_name="providers"
    )


class AuthProvider(sgqlc.types.Type):
    """The `AuthProvider` compound type represents an enabled OAuth
    Provider and associated metadata.
    """

    __schema__ = houston_schema
    __field_names__ = ("name", "display_name", "url")
    name = sgqlc.types.Field(String, graphql_name="name")

    display_name = sgqlc.types.Field(String, graphql_name="displayName")

    url = sgqlc.types.Field(String, graphql_name="url")


class AuthUser(sgqlc.types.Type):
    """The `AuthUser` compound type represents an authenticated user and
    associated metadata.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "user",
        "token",
        "permissions",
        "is_admin",
        "auth_user_capabilities",
    )
    user = sgqlc.types.Field("User", graphql_name="user")

    token = sgqlc.types.Field("Token", graphql_name="token")

    permissions = sgqlc.types.Field(JSON, graphql_name="permissions")

    is_admin = sgqlc.types.Field(Boolean, graphql_name="isAdmin")

    auth_user_capabilities = sgqlc.types.Field(
        "AuthUserCapabilities", graphql_name="authUserCapabilities"
    )


class AuthUserCapabilities(sgqlc.types.Type):
    """The `AuthUserCapabilities` compound type represents any system-
    scoped capabilities a user has.
    """

    __schema__ = houston_schema
    __field_names__ = ("can_sys_admin",)
    can_sys_admin = sgqlc.types.Field(Boolean, graphql_name="canSysAdmin")


class Card(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "name",
        "exp_month",
        "exp_year",
        "last4",
        "brand",
        "billing_email",
        "company",
    )
    name = sgqlc.types.Field(String, graphql_name="name")

    exp_month = sgqlc.types.Field(Int, graphql_name="expMonth")

    exp_year = sgqlc.types.Field(Int, graphql_name="expYear")

    last4 = sgqlc.types.Field(String, graphql_name="last4")

    brand = sgqlc.types.Field(String, graphql_name="brand")

    billing_email = sgqlc.types.Field(String, graphql_name="billingEmail")

    company = sgqlc.types.Field(String, graphql_name="company")


class ContainerResources(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("cpu", "memory")
    cpu = sgqlc.types.Field(Int, graphql_name="cpu")

    memory = sgqlc.types.Field(Int, graphql_name="memory")


class DeployInfo(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("current", "desired", "next_cli", "next")
    current = sgqlc.types.Field(String, graphql_name="current")

    desired = sgqlc.types.Field(String, graphql_name="desired")

    next_cli = sgqlc.types.Field(String, graphql_name="nextCli")

    next = sgqlc.types.Field(String, graphql_name="next")


class Deployment(sgqlc.types.Type):
    """The `Deployment` compound type represents a single Apache Airflow
    deployment in the platform.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "executor",
        "workers",
        "webserver",
        "scheduler",
        "config",
        "environment_variables",
        "properties",
        "urls",
        "alert_emails",
        "description",
        "label",
        "release_name",
        "status",
        "type",
        "version",
        "airflow_version",
        "desired_airflow_version",
        "deploy_info",
        "deployment_status",
        "workspace",
        "created_at",
        "updated_at",
        "role_bindings",
        "deployment_capabilities",
        "service_accounts",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")
    """A unique ID for the `Deployment`."""

    executor = sgqlc.types.Field(ExecutorType, graphql_name="executor")

    workers = sgqlc.types.Field("WorkersConfig", graphql_name="workers")

    webserver = sgqlc.types.Field("WebserverConfig", graphql_name="webserver")

    scheduler = sgqlc.types.Field("SchedulerConfig", graphql_name="scheduler")

    config = sgqlc.types.Field(JSON, graphql_name="config")

    environment_variables = sgqlc.types.Field(
        sgqlc.types.list_of("EnvironmentVariable"), graphql_name="environmentVariables"
    )
    """A list of user-configured `EnvironmentVariable`s for the
    `Deployment`.
    """

    properties = sgqlc.types.Field(JSON, graphql_name="properties")

    urls = sgqlc.types.Field(sgqlc.types.list_of("DeploymentUrl"), graphql_name="urls")
    """A list of `DeploymentUrl`s for the `Deployment`. These are the
    location of any webservers exposed for the `Deployment`.
    """

    alert_emails = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))),
        graphql_name="alertEmails",
    )

    description = sgqlc.types.Field(String, graphql_name="description")
    """A user-provided description of the `Deployment`."""

    label = sgqlc.types.Field(String, graphql_name="label")
    """A user-provided label of the `Deployment`."""

    release_name = sgqlc.types.Field(String, graphql_name="releaseName")
    """A unique release name for the `Deployment`. This corresponds to
    the helm release of the `Deployment`.
    """

    status = sgqlc.types.Field(String, graphql_name="status")
    """The status of the `Deployment`."""

    type = sgqlc.types.Field(String, graphql_name="type")
    """The type of the `Deployment`."""

    version = sgqlc.types.Field(String, graphql_name="version")
    """The version of the Airflow Helm Chart that the `Deployment` is
    running.
    """

    airflow_version = sgqlc.types.Field(String, graphql_name="airflowVersion")
    """The version of Airflow that the `Deployment` is running."""

    desired_airflow_version = sgqlc.types.Field(
        String, graphql_name="desiredAirflowVersion"
    )

    deploy_info = sgqlc.types.Field(DeployInfo, graphql_name="deployInfo")
    """Information about the running Airflow image for the `Deployment`."""

    deployment_status = sgqlc.types.Field(
        "DeploymentStatus", graphql_name="deploymentStatus"
    )

    workspace = sgqlc.types.Field("Workspace", graphql_name="workspace")
    """The `Workspace` that the `Deployment` belongs to."""

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )
    """The `DateTime` that the `Deployment` was created."""

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )
    """The `DateTime` that the `Deployment` was last updated."""

    role_bindings = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null("RoleBinding"))),
        graphql_name="roleBindings",
    )
    """A list of `RoleBinding`s attached to the `Deployment`. This
    determines who has access on the `Deployment`.
    """

    deployment_capabilities = sgqlc.types.Field(
        "DeploymentCapabilities", graphql_name="deploymentCapabilities"
    )
    """An object containing various `Boolean`s indicating what the
    current user can access in relation to the `Deployment`.
    """

    service_accounts = sgqlc.types.Field(
        sgqlc.types.list_of("ServiceAccount"), graphql_name="serviceAccounts"
    )
    """A list of `ServiceAccount`s that belong to the `Deployment`."""


class DeploymentCapabilities(sgqlc.types.Type):
    """The `DeploymentCapabilities` type is an enumeration of deployment-
    scoped capabilities within the system. These `Boolean` values are
    mostly driven from Astronomer `permissions` in the configuration
    file. Some capabilities take other server-side information into
    account.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "can_deploy",
        "can_update_deployment",
        "can_delete_deployment",
        "can_create_service_account",
        "can_update_service_account",
        "can_delete_service_account",
        "can_update_variables",
        "can_update_user_role",
    )
    can_deploy = sgqlc.types.Field(Boolean, graphql_name="canDeploy")
    """Can the current user deploy code to the `Deployment`?"""

    can_update_deployment = sgqlc.types.Field(
        Boolean, graphql_name="canUpdateDeployment"
    )
    """Can the current user update the `Deployment`?"""

    can_delete_deployment = sgqlc.types.Field(
        Boolean, graphql_name="canDeleteDeployment"
    )
    """Can the current user delete the `Deployment`?"""

    can_create_service_account = sgqlc.types.Field(
        Boolean, graphql_name="canCreateServiceAccount"
    )
    """Can the current user create a `ServiceAccount` for the
    `Deployment`?
    """

    can_update_service_account = sgqlc.types.Field(
        Boolean, graphql_name="canUpdateServiceAccount"
    )
    """Can the current user update a `ServiceAccount` in the
    `Deployment`?
    """

    can_delete_service_account = sgqlc.types.Field(
        Boolean, graphql_name="canDeleteServiceAccount"
    )
    """Can the current user delete a `ServiceAccount` from the
    `Deployment`?
    """

    can_update_variables = sgqlc.types.Field(Boolean, graphql_name="canUpdateVariables")

    can_update_user_role = sgqlc.types.Field(Boolean, graphql_name="canUpdateUserRole")
    """Can the current user update a user `Role` for the `Deployment`?"""


class DeploymentConfig(sgqlc.types.Type):
    """The `DeploymentConfig` compound type contains data describing
    available options for Airflow deployments in the system.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "defaults",
        "limits",
        "astro_unit",
        "max_extra_au",
        "executors",
        "single_namespace",
        "logging_enabled",
        "latest_version",
        "airflow_images",
        "airflow_versions",
        "default_airflow_image_tag",
        "default_airflow_chart_version",
    )
    defaults = sgqlc.types.Field(JSON, graphql_name="defaults")

    limits = sgqlc.types.Field(JSON, graphql_name="limits")

    astro_unit = sgqlc.types.Field(AstroUnit, graphql_name="astroUnit")

    max_extra_au = sgqlc.types.Field(Int, graphql_name="maxExtraAu")

    executors = sgqlc.types.Field(JSON, graphql_name="executors")

    single_namespace = sgqlc.types.Field(Boolean, graphql_name="singleNamespace")

    logging_enabled = sgqlc.types.Field(Boolean, graphql_name="loggingEnabled")

    latest_version = sgqlc.types.Field(String, graphql_name="latestVersion")

    airflow_images = sgqlc.types.Field(
        sgqlc.types.list_of(AirflowImage), graphql_name="airflowImages"
    )

    airflow_versions = sgqlc.types.Field(JSON, graphql_name="airflowVersions")

    default_airflow_image_tag = sgqlc.types.Field(
        String, graphql_name="defaultAirflowImageTag"
    )

    default_airflow_chart_version = sgqlc.types.Field(
        String, graphql_name="defaultAirflowChartVersion"
    )


class DeploymentLog(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("id", "timestamp", "release", "component", "level", "message")
    id = sgqlc.types.Field(String, graphql_name="id")

    timestamp = sgqlc.types.Field(String, graphql_name="timestamp")

    release = sgqlc.types.Field(String, graphql_name="release")

    component = sgqlc.types.Field(String, graphql_name="component")

    level = sgqlc.types.Field(String, graphql_name="level")

    message = sgqlc.types.Field(String, graphql_name="message")


class DeploymentMetric(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("label", "result")
    label = sgqlc.types.Field(String, graphql_name="label")

    result = sgqlc.types.Field(JSON, graphql_name="result")


class DeploymentStatus(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("status",)
    status = sgqlc.types.Field(DeploymentStatusType, graphql_name="status")


class DeploymentUrl(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("type", "url")
    type = sgqlc.types.Field(String, graphql_name="type")

    url = sgqlc.types.Field(String, graphql_name="url")


class DockerImage(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "name",
        "labels",
        "env",
        "tag",
        "digest",
        "deployment",
        "created_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    name = sgqlc.types.Field(String, graphql_name="name")

    labels = sgqlc.types.Field(JSON, graphql_name="labels")

    env = sgqlc.types.Field(JSON, graphql_name="env")

    tag = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="tag")

    digest = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="digest")

    deployment = sgqlc.types.Field(Deployment, graphql_name="deployment")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )


class Email(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "address",
        "primary",
        "token",
        "user",
        "verified",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    address = sgqlc.types.Field(String, graphql_name="address")

    primary = sgqlc.types.Field(Boolean, graphql_name="primary")

    token = sgqlc.types.Field(String, graphql_name="token")

    user = sgqlc.types.Field("User", graphql_name="user")

    verified = sgqlc.types.Field(Boolean, graphql_name="verified")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )


class EnvironmentVariable(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("key", "value", "is_secret")
    key = sgqlc.types.Field(String, graphql_name="key")

    value = sgqlc.types.Field(String, graphql_name="value")

    is_secret = sgqlc.types.Field(Boolean, graphql_name="isSecret")


class Invite(sgqlc.types.Type):
    """The `Invite` compound type represents an invitation to the
    platform.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "uuid",
        "assignments",
        "role",
        "email",
        "token",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(String, graphql_name="id")

    uuid = sgqlc.types.Field(String, graphql_name="uuid")

    assignments = sgqlc.types.Field(String, graphql_name="assignments")

    role = sgqlc.types.Field(String, graphql_name="role")

    email = sgqlc.types.Field(String, graphql_name="email")

    token = sgqlc.types.Field(String, graphql_name="token")

    created_at = sgqlc.types.Field(DateTime, graphql_name="createdAt")

    updated_at = sgqlc.types.Field(DateTime, graphql_name="updatedAt")


class LocalCredential(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "user",
        "password",
        "reset_token",
        "created_at",
        "updated_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    user = sgqlc.types.Field(sgqlc.types.non_null("User"), graphql_name="user")

    password = sgqlc.types.Field(String, graphql_name="password")

    reset_token = sgqlc.types.Field(String, graphql_name="resetToken")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )


class Metric(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("label", "result")
    label = sgqlc.types.Field(String, graphql_name="label")

    result = sgqlc.types.Field(JSON, graphql_name="result")


class Mutation(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "create_user",
        "confirm_email",
        "create_token",
        "forgot_password",
        "resend_confirmation",
        "reset_password",
        "create_deployment",
        "update_deployment",
        "update_deployment_keda_config",
        "update_deployment_airflow",
        "deployment_alerts_update",
        "deployment_add_user_role",
        "deployment_remove_user_role",
        "deployment_update_user_role",
        "delete_deployment",
        "delete_workspace",
        "update_self",
        "remove_user",
        "create_workspace",
        "workspace_add_user",
        "workspace_update_user_role",
        "workspace_remove_user",
        "delete_invite_token",
        "update_workspace",
        "upgrade_deployment",
        "create_service_account",
        "create_deployment_service_account",
        "create_workspace_service_account",
        "create_system_service_account",
        "update_service_account",
        "update_workspace_service_account",
        "update_deployment_service_account",
        "delete_service_account",
        "delete_workspace_service_account",
        "delete_deployment_service_account",
        "delete_system_service_account",
        "update_deployment_variables",
        "create_system_role_binding",
        "delete_system_role_binding",
        "invite_user",
        "add_card",
        "add_customer_id",
        "update_card",
        "suspend_workspace",
        "extend_workspace_trial",
        "verify_email",
    )
    create_user = sgqlc.types.Field(
        AuthUser,
        graphql_name="createUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
                (
                    "password",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="password",
                        default=None,
                    ),
                ),
                (
                    "username",
                    sgqlc.types.Arg(String, graphql_name="username", default=None),
                ),
                (
                    "profile",
                    sgqlc.types.Arg(JSON, graphql_name="profile", default=None),
                ),
                (
                    "invite_token",
                    sgqlc.types.Arg(String, graphql_name="inviteToken", default=None),
                ),
                (
                    "duration",
                    sgqlc.types.Arg(Int, graphql_name="duration", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    * `password` (`String!`)None
    * `username` (`String`)None
    * `profile` (`JSON`)None
    * `invite_token` (`String`)None
    * `duration` (`Int`)None
    """

    confirm_email = sgqlc.types.Field(
        AuthUser,
        graphql_name="confirmEmail",
        args=sgqlc.types.ArgDict(
            (
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="token", default=None
                    ),
                ),
                (
                    "duration",
                    sgqlc.types.Arg(Int, graphql_name="duration", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `token` (`String!`)None
    * `duration` (`Int`)None
    """

    create_token = sgqlc.types.Field(
        AuthUser,
        graphql_name="createToken",
        args=sgqlc.types.ArgDict(
            (
                (
                    "password",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="password",
                        default=None,
                    ),
                ),
                (
                    "identity",
                    sgqlc.types.Arg(String, graphql_name="identity", default=None),
                ),
                (
                    "duration",
                    sgqlc.types.Arg(Int, graphql_name="duration", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `password` (`String!`)None
    * `identity` (`String`)None
    * `duration` (`Int`)None
    """

    forgot_password = sgqlc.types.Field(
        Boolean,
        graphql_name="forgotPassword",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    """

    resend_confirmation = sgqlc.types.Field(
        Boolean,
        graphql_name="resendConfirmation",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    """

    reset_password = sgqlc.types.Field(
        AuthUser,
        graphql_name="resetPassword",
        args=sgqlc.types.ArgDict(
            (
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="token", default=None
                    ),
                ),
                (
                    "password",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="password",
                        default=None,
                    ),
                ),
                (
                    "duration",
                    sgqlc.types.Arg(Int, graphql_name="duration", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `token` (`String!`)None
    * `password` (`String!`)None
    * `duration` (`Int`)None
    """

    create_deployment = sgqlc.types.Field(
        Deployment,
        graphql_name="createDeployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "release_name",
                    sgqlc.types.Arg(String, graphql_name="releaseName", default=None),
                ),
                (
                    "type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="type", default=None
                    ),
                ),
                (
                    "label",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="label", default=None
                    ),
                ),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
                (
                    "version",
                    sgqlc.types.Arg(String, graphql_name="version", default=None),
                ),
                (
                    "airflow_version",
                    sgqlc.types.Arg(
                        String, graphql_name="airflowVersion", default=None
                    ),
                ),
                (
                    "executor",
                    sgqlc.types.Arg(
                        ExecutorType, graphql_name="executor", default=None
                    ),
                ),
                (
                    "workers",
                    sgqlc.types.Arg(Workers, graphql_name="workers", default=None),
                ),
                (
                    "webserver",
                    sgqlc.types.Arg(Webserver, graphql_name="webserver", default=None),
                ),
                (
                    "scheduler",
                    sgqlc.types.Arg(Scheduler, graphql_name="scheduler", default=None),
                ),
                ("config", sgqlc.types.Arg(JSON, graphql_name="config", default=None)),
                (
                    "properties",
                    sgqlc.types.Arg(JSON, graphql_name="properties", default=None),
                ),
                (
                    "cloud_role",
                    sgqlc.types.Arg(String, graphql_name="cloudRole", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `release_name` (`String`)None
    * `type` (`String!`)None
    * `label` (`String!`)None
    * `description` (`String`)None
    * `version` (`String`)None
    * `airflow_version` (`String`)None
    * `executor` (`ExecutorType`)None
    * `workers` (`Workers`)None
    * `webserver` (`Webserver`)None
    * `scheduler` (`Scheduler`)None
    * `config` (`JSON`)None
    * `properties` (`JSON`)None
    * `cloud_role` (`String`)None
    """

    update_deployment = sgqlc.types.Field(
        Deployment,
        graphql_name="updateDeployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "payload",
                    sgqlc.types.Arg(JSON, graphql_name="payload", default=None),
                ),
                (
                    "executor",
                    sgqlc.types.Arg(
                        ExecutorType, graphql_name="executor", default=None
                    ),
                ),
                (
                    "workers",
                    sgqlc.types.Arg(Workers, graphql_name="workers", default=None),
                ),
                (
                    "webserver",
                    sgqlc.types.Arg(Webserver, graphql_name="webserver", default=None),
                ),
                (
                    "scheduler",
                    sgqlc.types.Arg(Scheduler, graphql_name="scheduler", default=None),
                ),
                ("config", sgqlc.types.Arg(JSON, graphql_name="config", default=None)),
                ("sync", sgqlc.types.Arg(Boolean, graphql_name="sync", default=None)),
                (
                    "cloud_role",
                    sgqlc.types.Arg(String, graphql_name="cloudRole", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `payload` (`JSON`)None
    * `executor` (`ExecutorType`)None
    * `workers` (`Workers`)None
    * `webserver` (`Webserver`)None
    * `scheduler` (`Scheduler`)None
    * `config` (`JSON`)None
    * `sync` (`Boolean`)None
    * `cloud_role` (`String`)None
    """

    update_deployment_keda_config = sgqlc.types.Field(
        Deployment,
        graphql_name="updateDeploymentKedaConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "state",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="state",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `state` (`Boolean!`)None
    """

    update_deployment_airflow = sgqlc.types.Field(
        Deployment,
        graphql_name="updateDeploymentAirflow",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "desired_airflow_version",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="desiredAirflowVersion",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `desired_airflow_version` (`String!`)None
    """

    deployment_alerts_update = sgqlc.types.Field(
        Deployment,
        graphql_name="deploymentAlertsUpdate",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "alert_emails",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(String),
                        graphql_name="alertEmails",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `alert_emails` (`[String]`)None
    """

    deployment_add_user_role = sgqlc.types.Field(
        "RoleBinding",
        graphql_name="deploymentAddUserRole",
        args=sgqlc.types.ArgDict(
            (
                ("user_id", sgqlc.types.Arg(Id, graphql_name="userId", default=None)),
                (
                    "deployment_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Id),
                        graphql_name="deploymentId",
                        default=None,
                    ),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """The `deploymentAddUserRole` mutation adds an user role to a
    deployment and returns an `RoleBinding` type

    Arguments:

    * `user_id` (`Id`)None
    * `deployment_id` (`Id!`)None
    * `email` (`String!`)None
    * `role` (`Role!`)None
    """

    deployment_remove_user_role = sgqlc.types.Field(
        "RoleBinding",
        graphql_name="deploymentRemoveUserRole",
        args=sgqlc.types.ArgDict(
            (
                ("user_id", sgqlc.types.Arg(Id, graphql_name="userId", default=None)),
                (
                    "deployment_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Id),
                        graphql_name="deploymentId",
                        default=None,
                    ),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
            )
        ),
    )
    """The `deploymentRemoveUserRole` mutation removes an user role to a
    deployment and returns an `RoleBinding` type

    Arguments:

    * `user_id` (`Id`)None
    * `deployment_id` (`Id!`)None
    * `email` (`String!`)None
    """

    deployment_update_user_role = sgqlc.types.Field(
        "RoleBinding",
        graphql_name="deploymentUpdateUserRole",
        args=sgqlc.types.ArgDict(
            (
                ("user_id", sgqlc.types.Arg(Id, graphql_name="userId", default=None)),
                (
                    "deployment_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Id),
                        graphql_name="deploymentId",
                        default=None,
                    ),
                ),
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """The `deploymentUpdateUserRole` mutation updates an user role to a
    deployment and returns an `RoleBinding` type

    Arguments:

    * `user_id` (`Id`)None
    * `deployment_id` (`Id!`)None
    * `email` (`String!`)None
    * `role` (`Role!`)None
    """

    delete_deployment = sgqlc.types.Field(
        Deployment,
        graphql_name="deleteDeployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    """

    delete_workspace = sgqlc.types.Field(
        "Workspace",
        graphql_name="deleteWorkspace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    """

    update_self = sgqlc.types.Field(
        "User",
        graphql_name="updateSelf",
        args=sgqlc.types.ArgDict(
            (
                (
                    "payload",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSON), graphql_name="payload", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `payload` (`JSON!`)None
    """

    remove_user = sgqlc.types.Field(
        "User",
        graphql_name="removeUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="userUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `user_uuid` (`Uuid!`)None
    """

    create_workspace = sgqlc.types.Field(
        "Workspace",
        graphql_name="createWorkspace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "label",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="label", default=None
                    ),
                ),
                (
                    "description",
                    sgqlc.types.Arg(String, graphql_name="description", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `label` (`String!`)None
    * `description` (`String`)None
    """

    workspace_add_user = sgqlc.types.Field(
        "Workspace",
        graphql_name="workspaceAddUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="workspaceUuid", default=None),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role),
                        graphql_name="role",
                        default="WORKSPACE_VIEWER",
                    ),
                ),
                (
                    "deployment_roles",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(DeploymentRoles),
                        graphql_name="deploymentRoles",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    * `workspace_uuid` (`Uuid`)None
    * `role` (`Role!`)None (default: `WORKSPACE_VIEWER`)
    * `deployment_roles` (`[DeploymentRoles]`)None
    """

    workspace_update_user_role = sgqlc.types.Field(
        Role,
        graphql_name="workspaceUpdateUserRole",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    * `workspace_uuid` (`Uuid!`)None
    * `role` (`Role!`)None
    """

    workspace_remove_user = sgqlc.types.Field(
        "Workspace",
        graphql_name="workspaceRemoveUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="userUuid",
                        default=None,
                    ),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `user_uuid` (`Uuid!`)None
    * `workspace_uuid` (`Uuid!`)None
    """

    delete_invite_token = sgqlc.types.Field(
        Invite,
        graphql_name="deleteInviteToken",
        args=sgqlc.types.ArgDict(
            (
                (
                    "invite_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="inviteUuid", default=None),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="workspaceUuid", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `invite_uuid` (`Uuid`)None
    * `workspace_uuid` (`Uuid`)None
    """

    update_workspace = sgqlc.types.Field(
        "Workspace",
        graphql_name="updateWorkspace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "payload",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSON), graphql_name="payload", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `payload` (`JSON!`)None
    """

    upgrade_deployment = sgqlc.types.Field(
        Deployment,
        graphql_name="upgradeDeployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "version",
                    sgqlc.types.Arg(String, graphql_name="version", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `version` (`String`)None
    """

    create_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="createServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "label",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="label", default=None
                    ),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                (
                    "entity_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityType),
                        graphql_name="entityType",
                        default=None,
                    ),
                ),
                (
                    "entity_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="entityUuid", default=None),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `label` (`String!`)None
    * `category` (`String`)None
    * `entity_type` (`EntityType!`)None
    * `entity_uuid` (`Uuid`)None
    * `role` (`Role!`)None
    """

    create_deployment_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="createDeploymentServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "label",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="label", default=None
                    ),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `label` (`String!`)None
    * `category` (`String`)None
    * `deployment_uuid` (`Uuid!`)None
    * `role` (`Role!`)None
    """

    create_workspace_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="createWorkspaceServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "label",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="label", default=None
                    ),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `label` (`String!`)None
    * `category` (`String`)None
    * `workspace_uuid` (`Uuid!`)None
    * `role` (`Role!`)None
    """

    create_system_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="createSystemServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "label",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="label", default=None
                    ),
                ),
                (
                    "category",
                    sgqlc.types.Arg(String, graphql_name="category", default=None),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `label` (`String!`)None
    * `category` (`String`)None
    * `role` (`Role!`)None
    """

    update_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="updateServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
                (
                    "payload",
                    sgqlc.types.Arg(JSON, graphql_name="payload", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    * `payload` (`JSON`)None
    """

    update_workspace_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="updateWorkspaceServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "payload",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(JSON), graphql_name="payload", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    * `workspace_uuid` (`Uuid!`)None
    * `payload` (`JSON!`)None
    """

    update_deployment_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="updateDeploymentServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "payload",
                    sgqlc.types.Arg(JSON, graphql_name="payload", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    * `deployment_uuid` (`Uuid!`)None
    * `payload` (`JSON`)None
    """

    delete_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="deleteServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    """

    delete_workspace_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="deleteWorkspaceServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    * `workspace_uuid` (`Uuid!`)None
    """

    delete_deployment_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="deleteDeploymentServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    * `deployment_uuid` (`Uuid!`)None
    """

    delete_system_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="deleteSystemServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid!`)None
    """

    update_deployment_variables = sgqlc.types.Field(
        sgqlc.types.list_of(EnvironmentVariable),
        graphql_name="updateDeploymentVariables",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "release_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="releaseName",
                        default=None,
                    ),
                ),
                (
                    "environment_variables",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(
                            sgqlc.types.list_of(InputEnvironmentVariable)
                        ),
                        graphql_name="environmentVariables",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `release_name` (`String!`)None
    * `environment_variables` (`[InputEnvironmentVariable]!`)None
    """

    create_system_role_binding = sgqlc.types.Field(
        "RoleBinding",
        graphql_name="createSystemRoleBinding",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="userId", default=None
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `user_id` (`ID!`)None
    * `role` (`Role!`)None
    """

    delete_system_role_binding = sgqlc.types.Field(
        "RoleBinding",
        graphql_name="deleteSystemRoleBinding",
        args=sgqlc.types.ArgDict(
            (
                (
                    "user_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(ID), graphql_name="userId", default=None
                    ),
                ),
                (
                    "role",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Role), graphql_name="role", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `user_id` (`ID!`)None
    * `role` (`Role!`)None
    """

    invite_user = sgqlc.types.Field(
        Invite,
        graphql_name="inviteUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    """

    add_card = sgqlc.types.Field(
        Card,
        graphql_name="addCard",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "billing_email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="billingEmail",
                        default=None,
                    ),
                ),
                (
                    "company",
                    sgqlc.types.Arg(String, graphql_name="company", default=None),
                ),
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="token", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `billing_email` (`String!`)None
    * `company` (`String`)None
    * `token` (`String!`)None
    """

    add_customer_id = sgqlc.types.Field(
        "Workspace",
        graphql_name="addCustomerId",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "stripe_customer_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="stripeCustomerId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `stripe_customer_id` (`String!`)None
    """

    update_card = sgqlc.types.Field(
        Card,
        graphql_name="updateCard",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "billing_email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="billingEmail",
                        default=None,
                    ),
                ),
                (
                    "company",
                    sgqlc.types.Arg(String, graphql_name="company", default=None),
                ),
                (
                    "token",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="token", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `billing_email` (`String!`)None
    * `company` (`String`)None
    * `token` (`String!`)None
    """

    suspend_workspace = sgqlc.types.Field(
        "Workspace",
        graphql_name="suspendWorkspace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "is_suspended",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Boolean),
                        graphql_name="isSuspended",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `is_suspended` (`Boolean!`)None
    """

    extend_workspace_trial = sgqlc.types.Field(
        "Workspace",
        graphql_name="extendWorkspaceTrial",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "extra_days",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Int),
                        graphql_name="extraDays",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`)None
    * `extra_days` (`Int!`)None
    """

    verify_email = sgqlc.types.Field(
        Boolean,
        graphql_name="verifyEmail",
        args=sgqlc.types.ArgDict(
            (
                (
                    "email",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String), graphql_name="email", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `email` (`String!`)None
    """


class PlatformRelease(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("version", "url", "level", "description", "release_date")
    version = sgqlc.types.Field(String, graphql_name="version")
    """The new version of the platform that is available for download."""

    url = sgqlc.types.Field(String, graphql_name="url")
    """The URL of the git tag representing this release."""

    level = sgqlc.types.Field(String, graphql_name="level")
    """The level of the update. Eg: `bug_fix`, `new_feature`, etc."""

    description = sgqlc.types.Field(String, graphql_name="description")
    """A description of the new release."""

    release_date = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="releaseDate"
    )
    """The date when this new release was published."""


class Query(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "email",
        "workspace",
        "deployment",
        "airflow_release",
        "auth_config",
        "app_config",
        "self",
        "deployment_config",
        "workspaces",
        "update_available",
        "users",
        "deployments",
        "deployment_users",
        "deployment_variables",
        "invites",
        "airflow_releases",
        "card",
        "workspace_invites",
        "workspace_deployments",
        "workspace_deployment",
        "service_accounts",
        "workspace_service_accounts",
        "workspace_service_account",
        "workspace_users",
        "workspace_user",
        "deployment_service_account",
        "deployment_service_accounts",
        "logs",
    )
    email = sgqlc.types.Field(
        Email,
        graphql_name="email",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EmailWhereUniqueInput),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `where` (`EmailWhereUniqueInput!`)None
    """

    workspace = sgqlc.types.Field(
        "Workspace",
        graphql_name="workspace",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """The `workspace` query returns a single `Workspace` type, exposing
    information about a given `Workspace`.

    Arguments:

    * `workspace_uuid` (`Uuid!`)None
    """

    deployment = sgqlc.types.Field(
        Deployment,
        graphql_name="deployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(DeploymentWhereUniqueInput),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `where` (`DeploymentWhereUniqueInput!`)None
    """

    airflow_release = sgqlc.types.Field(
        AirflowRelease,
        graphql_name="airflowRelease",
        args=sgqlc.types.ArgDict(
            (
                (
                    "where",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(AirflowReleaseWhereUniqueInput),
                        graphql_name="where",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `where` (`AirflowReleaseWhereUniqueInput!`)None
    """

    auth_config = sgqlc.types.Field(
        AuthConfig,
        graphql_name="authConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "redirect",
                    sgqlc.types.Arg(String, graphql_name="redirect", default=None),
                ),
                (
                    "duration",
                    sgqlc.types.Arg(Int, graphql_name="duration", default=None),
                ),
                ("extras", sgqlc.types.Arg(JSON, graphql_name="extras", default=None)),
                (
                    "invite_token",
                    sgqlc.types.Arg(String, graphql_name="inviteToken", default=None),
                ),
            )
        ),
    )
    """The `authConfig` query returns an `AuthConfig` type, exposing some
    information about the current configuration of the authentication
    system.

    Arguments:

    * `redirect` (`String`)None
    * `duration` (`Int`)None
    * `extras` (`JSON`)None
    * `invite_token` (`String`)None
    """

    app_config = sgqlc.types.Field(AppConfig, graphql_name="appConfig")
    """The `appConfig` query returns an `AppConfig` type, exposing some
    basic platform-level configurations to clients.
    """

    self = sgqlc.types.Field(AuthUser, graphql_name="self")
    """The `self` query returns an `AuthUser` type, representing some
    information about the currently logged in user.
    """

    deployment_config = sgqlc.types.Field(
        DeploymentConfig,
        graphql_name="deploymentConfig",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="workspaceUuid", default=None),
                ),
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="deploymentUuid", default=None),
                ),
                ("type", sgqlc.types.Arg(String, graphql_name="type", default=None)),
                (
                    "version",
                    sgqlc.types.Arg(String, graphql_name="version", default=None),
                ),
            )
        ),
    )
    """The `deploymentConfig` query returns a `DeploymentConfig` object.

    Arguments:

    * `workspace_uuid` (`Uuid`): A `Workspace` id.
    * `deployment_uuid` (`Uuid`): A `Deployment` id.
    * `type` (`String`): The type of deployment.
    * `version` (`String`): The version of deployment.
    """

    workspaces = sgqlc.types.Field(
        sgqlc.types.list_of("Workspace"), graphql_name="workspaces"
    )
    """The `workspaces` query returns a list of `Workspace`s that the
    current user has access to.
    """

    update_available = sgqlc.types.Field(
        PlatformRelease, graphql_name="updateAvailable"
    )

    users = sgqlc.types.Field(
        sgqlc.types.list_of("User"),
        graphql_name="users",
        args=sgqlc.types.ArgDict(
            (("user", sgqlc.types.Arg(UserSearch, graphql_name="user", default=None)),)
        ),
    )
    """Arguments:

    * `user` (`UserSearch`)None
    """

    deployments = sgqlc.types.Field(
        sgqlc.types.list_of(Deployment), graphql_name="deployments"
    )
    """The `deployments` query returns a list of `Deployment`s that the
    current user has access to.
    """

    deployment_users = sgqlc.types.Field(
        sgqlc.types.list_of("User"),
        graphql_name="deploymentUsers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Id),
                        graphql_name="deploymentId",
                        default=None,
                    ),
                ),
                (
                    "user",
                    sgqlc.types.Arg(UserSearch, graphql_name="user", default=None),
                ),
            )
        ),
    )
    """The `deploymentUsers` query returns a list of `Users`s of a
    particular deployment

    Arguments:

    * `deployment_id` (`Id!`)None
    * `user` (`UserSearch`): A `UserSearch` input type.
    """

    deployment_variables = sgqlc.types.Field(
        sgqlc.types.list_of(EnvironmentVariable),
        graphql_name="deploymentVariables",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "release_name",
                    sgqlc.types.Arg(String, graphql_name="releaseName", default=None),
                ),
            )
        ),
    )
    """The `deploymentVariables` query returns a list of
    `EnvironmentVariable`s configured for a given `Deployment`

    Arguments:

    * `deployment_uuid` (`Uuid!`): A `Workspace` id.
    * `release_name` (`String`): A release name of a `Deployment`.
    """

    invites = sgqlc.types.Field(
        sgqlc.types.list_of(Invite),
        graphql_name="invites",
        args=sgqlc.types.ArgDict(
            (
                (
                    "invite",
                    sgqlc.types.Arg(InviteSearch, graphql_name="invite", default=None),
                ),
            )
        ),
    )
    """The `invites` query returns a list of `Invite`s for the given
    search critera.

    Arguments:

    * `invite` (`InviteSearch`): An `InviteSearch` input type.
    """

    airflow_releases = sgqlc.types.Field(
        sgqlc.types.list_of(AirflowRelease), graphql_name="airflowReleases"
    )

    card = sgqlc.types.Field(
        Card,
        graphql_name="card",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "stripe_customer_id",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="stripeCustomerId",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Return the Credit Card details for a given `Workspace`.

    Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `stripe_customer_id` (`String!`):  A customer id in Stripe.
    """

    workspace_invites = sgqlc.types.Field(
        sgqlc.types.list_of(Invite),
        graphql_name="workspaceInvites",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "invite",
                    sgqlc.types.Arg(InviteSearch, graphql_name="invite", default=None),
                ),
            )
        ),
    )
    """The `workspaceInvites` query returns a list of `Invite`s for the
    given `Workspace`.

    Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `invite` (`InviteSearch`): An `InviteSearch` input type.
    """

    workspace_deployments = sgqlc.types.Field(
        sgqlc.types.list_of(Deployment),
        graphql_name="workspaceDeployments",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "release_name",
                    sgqlc.types.Arg(String, graphql_name="releaseName", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `release_name` (`String`): A release name of a `Deployment`.
    """

    workspace_deployment = sgqlc.types.Field(
        Deployment,
        graphql_name="workspaceDeployment",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "release_name",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(String),
                        graphql_name="releaseName",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `release_name` (`String!`): A release name of a `Deployment`.
    """

    service_accounts = sgqlc.types.Field(
        sgqlc.types.list_of("ServiceAccount"),
        graphql_name="serviceAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        Uuid, graphql_name="serviceAccountUuid", default=None
                    ),
                ),
                (
                    "entity_type",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(EntityType),
                        graphql_name="entityType",
                        default=None,
                    ),
                ),
                (
                    "entity_uuid",
                    sgqlc.types.Arg(Uuid, graphql_name="entityUuid", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `service_account_uuid` (`Uuid`)None
    * `entity_type` (`EntityType!`)None
    * `entity_uuid` (`Uuid`)None
    """

    workspace_service_accounts = sgqlc.types.Field(
        sgqlc.types.list_of("ServiceAccount"),
        graphql_name="workspaceServiceAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """The `workspaceServiceAccounts` query returns a list of
    `ServiceAccount`s for the given `Workspace`.

    Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    """

    workspace_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="workspaceServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """The `workspaceServiceAccount` query returns the requested
    `ServiceAccount`.

    Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `service_account_uuid` (`Uuid!`): A `ServiceAccount` id.
    """

    workspace_users = sgqlc.types.Field(
        sgqlc.types.list_of("User"),
        graphql_name="workspaceUsers",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "user",
                    sgqlc.types.Arg(UserSearch, graphql_name="user", default=None),
                ),
            )
        ),
    )
    """The `workspaceUsers` query returns a list of `User`s for the given
    `Workspace`.

    Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `user` (`UserSearch`): A `UserSearch` input type.
    """

    workspace_user = sgqlc.types.Field(
        "User",
        graphql_name="workspaceUser",
        args=sgqlc.types.ArgDict(
            (
                (
                    "workspace_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="workspaceUuid",
                        default=None,
                    ),
                ),
                (
                    "user",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(UserSearch),
                        graphql_name="user",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """The `workspaceUser` query returns the requested `User` for the
    given `Workspace`.

    Arguments:

    * `workspace_uuid` (`Uuid!`): A `Workspace` id.
    * `user` (`UserSearch!`): A `UserSearch` input type.
    """

    deployment_service_account = sgqlc.types.Field(
        "ServiceAccount",
        graphql_name="deploymentServiceAccount",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "service_account_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="serviceAccountUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """The `deploymentServiceAccount` query returns the requested
    `ServiceAccount` for the given `Deployment`.

    Arguments:

    * `deployment_uuid` (`Uuid!`): A `Deployment` id.
    * `service_account_uuid` (`Uuid!`): A `ServiceAccount` id.
    """

    deployment_service_accounts = sgqlc.types.Field(
        sgqlc.types.list_of("ServiceAccount"),
        graphql_name="deploymentServiceAccounts",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
            )
        ),
    )
    """The `deploymentServiceAccounts` query returns a list of
    `ServiceAccount`s for then given `Deployment`.

    Arguments:

    * `deployment_uuid` (`Uuid!`): A `Deployment` id.
    """

    logs = sgqlc.types.Field(
        sgqlc.types.list_of(DeploymentLog),
        graphql_name="logs",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "component",
                    sgqlc.types.Arg(String, graphql_name="component", default=None),
                ),
                (
                    "timestamp",
                    sgqlc.types.Arg(DateTime, graphql_name="timestamp", default=None),
                ),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """The `logs` query returns log lines from Elasticsearch for a given
    `Deployment`.

    Arguments:

    * `deployment_uuid` (`Uuid!`): A `Deployment` id.
    * `component` (`String`): A component name. Eg: webserver,
      scheduler, worker.
    * `timestamp` (`DateTime`): A `DateTime` representing the start
      date on the query.
    * `search` (`String`): A `String` to search for within the log
      lines.
    """


class ReplicaLimits(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("default", "minimum", "limit", "min_airflow_version")
    default = sgqlc.types.Field(Int, graphql_name="default")

    minimum = sgqlc.types.Field(Int, graphql_name="minimum")

    limit = sgqlc.types.Field(Int, graphql_name="limit")

    min_airflow_version = sgqlc.types.Field(String, graphql_name="minAirflowVersion")


class ResourcesLimits(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("requests", "limits")
    requests = sgqlc.types.Field(ContainerResources, graphql_name="requests")

    limits = sgqlc.types.Field(ContainerResources, graphql_name="limits")


class RoleBinding(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "role",
        "user",
        "service_account",
        "workspace",
        "deployment",
        "created_at",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    role = sgqlc.types.Field(Role, graphql_name="role")

    user = sgqlc.types.Field("User", graphql_name="user")

    service_account = sgqlc.types.Field("ServiceAccount", graphql_name="serviceAccount")

    workspace = sgqlc.types.Field("Workspace", graphql_name="workspace")

    deployment = sgqlc.types.Field(Deployment, graphql_name="deployment")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )


class SchedulerConfig(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("replicas", "resources")
    replicas = sgqlc.types.Field(ReplicaLimits, graphql_name="replicas")

    resources = sgqlc.types.Field(ResourcesLimits, graphql_name="resources")


class ServiceAccount(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "api_key",
        "label",
        "category",
        "entity_type",
        "entity_uuid",
        "workspace_uuid",
        "deployment_uuid",
        "active",
        "last_used_at",
        "created_at",
        "updated_at",
        "role_bindings",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")

    api_key = sgqlc.types.Field(String, graphql_name="apiKey")

    label = sgqlc.types.Field(String, graphql_name="label")

    category = sgqlc.types.Field(String, graphql_name="category")

    entity_type = sgqlc.types.Field(String, graphql_name="entityType")

    entity_uuid = sgqlc.types.Field(Uuid, graphql_name="entityUuid")

    workspace_uuid = sgqlc.types.Field(Uuid, graphql_name="workspaceUuid")

    deployment_uuid = sgqlc.types.Field(Uuid, graphql_name="deploymentUuid")

    active = sgqlc.types.Field(Boolean, graphql_name="active")

    last_used_at = sgqlc.types.Field(DateTime, graphql_name="lastUsedAt")

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )

    role_bindings = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleBinding))),
        graphql_name="roleBindings",
        args=sgqlc.types.ArgDict(
            (
                ("first", sgqlc.types.Arg(Int, graphql_name="first", default=None)),
                ("last", sgqlc.types.Arg(Int, graphql_name="last", default=None)),
                (
                    "before",
                    sgqlc.types.Arg(
                        RoleBindingWhereUniqueInput, graphql_name="before", default=None
                    ),
                ),
                (
                    "after",
                    sgqlc.types.Arg(
                        RoleBindingWhereUniqueInput, graphql_name="after", default=None
                    ),
                ),
            )
        ),
    )
    """Arguments:

    * `first` (`Int`)None
    * `last` (`Int`)None
    * `before` (`RoleBindingWhereUniqueInput`)None
    * `after` (`RoleBindingWhereUniqueInput`)None
    """


class Subscription(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("deployment_status", "log", "metrics")
    deployment_status = sgqlc.types.Field(
        DeploymentStatus,
        graphql_name="deploymentStatus",
        args=sgqlc.types.ArgDict(
            (
                (
                    "release_name",
                    sgqlc.types.Arg(String, graphql_name="releaseName", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `release_name` (`String`)None
    """

    log = sgqlc.types.Field(
        DeploymentLog,
        graphql_name="log",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "component",
                    sgqlc.types.Arg(String, graphql_name="component", default=None),
                ),
                (
                    "timestamp",
                    sgqlc.types.Arg(DateTime, graphql_name="timestamp", default=None),
                ),
                (
                    "search",
                    sgqlc.types.Arg(String, graphql_name="search", default=None),
                ),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `component` (`String`)None
    * `timestamp` (`DateTime`)None
    * `search` (`String`)None
    """

    metrics = sgqlc.types.Field(
        sgqlc.types.list_of(Metric),
        graphql_name="metrics",
        args=sgqlc.types.ArgDict(
            (
                (
                    "deployment_uuid",
                    sgqlc.types.Arg(
                        sgqlc.types.non_null(Uuid),
                        graphql_name="deploymentUuid",
                        default=None,
                    ),
                ),
                (
                    "metric_type",
                    sgqlc.types.Arg(
                        sgqlc.types.list_of(MetricType),
                        graphql_name="metricType",
                        default=None,
                    ),
                ),
                ("since", sgqlc.types.Arg(Int, graphql_name="since", default=None)),
                ("step", sgqlc.types.Arg(Int, graphql_name="step", default=None)),
            )
        ),
    )
    """Arguments:

    * `deployment_uuid` (`Uuid!`)None
    * `metric_type` (`[MetricType]`)None
    * `since` (`Int`)None
    * `step` (`Int`)None
    """


class Token(sgqlc.types.Type):
    """The `Token` compound type contains an Astronomer JWT and
    associated properties.
    """

    __schema__ = houston_schema
    __field_names__ = ("value", "payload")
    value = sgqlc.types.Field(String, graphql_name="value")

    payload = sgqlc.types.Field("TokenPayload", graphql_name="payload")


class TokenPayload(sgqlc.types.Type):
    """The `TokenPayload` compound type contains plaintext claims from an
    Astronomer JWT.
    """

    __schema__ = houston_schema
    __field_names__ = ("uuid", "iat", "exp")
    uuid = sgqlc.types.Field(Uuid, graphql_name="uuid")

    iat = sgqlc.types.Field(Int, graphql_name="iat")

    exp = sgqlc.types.Field(Int, graphql_name="exp")


class User(sgqlc.types.Type):
    """The `User` compound type represents a user in the system."""

    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "username",
        "emails",
        "full_name",
        "status",
        "profile",
        "created_at",
        "updated_at",
        "role_bindings",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")
    """A unique ID of the `User`."""

    username = sgqlc.types.Field(String, graphql_name="username")
    """The username of the `User`."""

    emails = sgqlc.types.Field(sgqlc.types.list_of(Email), graphql_name="emails")
    """A list of `Email`s associated with the `User`."""

    full_name = sgqlc.types.Field(String, graphql_name="fullName")
    """The full name of the `User`."""

    status = sgqlc.types.Field(String, graphql_name="status")
    """The status of the `User`."""

    profile = sgqlc.types.Field(sgqlc.types.list_of("UserProp"), graphql_name="profile")
    """The profile of the `User`."""

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )
    """The `DateTime` that the `User` was created."""

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )
    """The `DateTime` that the `User` was last updated."""

    role_bindings = sgqlc.types.Field(
        sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(RoleBinding))),
        graphql_name="roleBindings",
    )
    """A list of `RoleBinding`s attached to the `User`. This determines
    what `Deployment` and `Workspace`s the `User` has access to.
    """


class UserProp(sgqlc.types.Type):
    """The `UserProp` compound type contains a key / value pair
    representing a field on a user profile.
    """

    __schema__ = houston_schema
    __field_names__ = ("key", "value", "category")
    key = sgqlc.types.Field(String, graphql_name="key")

    value = sgqlc.types.Field(String, graphql_name="value")

    category = sgqlc.types.Field(String, graphql_name="category")


class WebserverConfig(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("resources", "use_default_airflow_image")
    resources = sgqlc.types.Field(ResourcesLimits, graphql_name="resources")

    use_default_airflow_image = sgqlc.types.Field(
        Boolean, graphql_name="useDefaultAirflowImage"
    )


class WorkersConfig(sgqlc.types.Type):
    __schema__ = houston_schema
    __field_names__ = ("replicas", "termination_grace_period_seconds", "resources")
    replicas = sgqlc.types.Field(Int, graphql_name="replicas")

    termination_grace_period_seconds = sgqlc.types.Field(
        Int, graphql_name="terminationGracePeriodSeconds"
    )

    resources = sgqlc.types.Field(ResourcesLimits, graphql_name="resources")


class Workspace(sgqlc.types.Type):
    """The `Workspace` type represents a workspace in the system.
    Workspaces also function as "teams" and are the entity that is
    attached to a credit card in cloud mode.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "id",
        "deployments",
        "active",
        "description",
        "invites",
        "properties",
        "label",
        "users",
        "stripe_customer_id",
        "role_bindings",
        "workspace_capabilities",
        "created_at",
        "updated_at",
        "trial_ends_at",
        "billing_enabled",
        "service_accounts",
        "paywall_enabled",
    )
    id = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name="id")
    """A unique ID for the `Workspace`."""

    deployments = sgqlc.types.Field(
        sgqlc.types.list_of(Deployment), graphql_name="deployments"
    )

    active = sgqlc.types.Field(Boolean, graphql_name="active")
    """Is the `Workspace` active?"""

    description = sgqlc.types.Field(String, graphql_name="description")
    """A user-provided description of the `Workspace`."""

    invites = sgqlc.types.Field(Invite, graphql_name="invites")
    """A list of `Invite`s to the `Workspace`."""

    properties = sgqlc.types.Field(JSON, graphql_name="properties")
    """A user-provided label of the `Workspace`."""

    label = sgqlc.types.Field(String, graphql_name="label")
    """A user-provided label of the `Workspace`."""

    users = sgqlc.types.Field(sgqlc.types.list_of(User), graphql_name="users")
    """A list of `User`s who have access to the `Workspace`."""

    stripe_customer_id = sgqlc.types.Field(String, graphql_name="stripeCustomerId")
    """The customer ID in Stripe that is attatched to the `Workspace`."""

    role_bindings = sgqlc.types.Field(
        sgqlc.types.list_of(RoleBinding), graphql_name="roleBindings"
    )

    workspace_capabilities = sgqlc.types.Field(
        "WorkspaceCapabilities", graphql_name="workspaceCapabilities"
    )
    """An object containing various `Boolean`s indicating what the
    current user can access in relation to the `Workspace`.
    """

    created_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="createdAt"
    )
    """The `DateTime` that the `Workspace` was created."""

    updated_at = sgqlc.types.Field(
        sgqlc.types.non_null(DateTime), graphql_name="updatedAt"
    )
    """The `DateTime` that the `Workspace` was last updated."""

    trial_ends_at = sgqlc.types.Field(DateTime, graphql_name="trialEndsAt")
    """The `DateTime` that the `Workspace` trial will expire."""

    billing_enabled = sgqlc.types.Field(Boolean, graphql_name="billingEnabled")
    """Is billing enabled for the `Workspace`?"""

    service_accounts = sgqlc.types.Field(
        sgqlc.types.list_of(ServiceAccount), graphql_name="serviceAccounts"
    )
    """A list of `ServiceAccount`s that belong to the `Workspace`."""

    paywall_enabled = sgqlc.types.Field(Boolean, graphql_name="paywallEnabled")
    """Should the paywall be displayed to users of the `Workspace`?"""


class WorkspaceCapabilities(sgqlc.types.Type):
    """The `WorkspaceCapabilities` type is an enumeration of workspace-
    scoped capabilities within the system. These `Boolean` values are
    mostly driven from Astronomer `permissions` in the configuration
    file. Some capabilities take other server-side information into
    account.
    """

    __schema__ = houston_schema
    __field_names__ = (
        "can_update_billing",
        "can_update_iam",
        "can_update_workspace",
        "can_delete_workspace",
        "can_create_deployment",
        "can_invite_user",
        "can_update_user",
        "can_delete_user",
        "can_create_service_account",
        "can_update_service_account",
        "can_delete_service_account",
    )
    can_update_billing = sgqlc.types.Field(Boolean, graphql_name="canUpdateBilling")
    """Can the current user update billing information on the
    `Workspace`?
    """

    can_update_iam = sgqlc.types.Field(Boolean, graphql_name="canUpdateIAM")
    """Can the current user update IAM information on the `Workspace`?"""

    can_update_workspace = sgqlc.types.Field(Boolean, graphql_name="canUpdateWorkspace")
    """Can the current user read information on the `Workspace`?"""

    can_delete_workspace = sgqlc.types.Field(Boolean, graphql_name="canDeleteWorkspace")
    """Can the current user update the `Workspace`?"""

    can_create_deployment = sgqlc.types.Field(
        Boolean, graphql_name="canCreateDeployment"
    )
    """Can the current user delete the `Workspace`?"""

    can_invite_user = sgqlc.types.Field(Boolean, graphql_name="canInviteUser")
    """Can the current user create a `Deployment` in the `Workspace`?"""

    can_update_user = sgqlc.types.Field(Boolean, graphql_name="canUpdateUser")
    """Can the current user invite a user to the `Workspace`?"""

    can_delete_user = sgqlc.types.Field(Boolean, graphql_name="canDeleteUser")
    """Can the current user update a `User` in the `Workspace`?"""

    can_create_service_account = sgqlc.types.Field(
        Boolean, graphql_name="canCreateServiceAccount"
    )
    """Can the current user delete a `User` from the `Workspace`?"""

    can_update_service_account = sgqlc.types.Field(
        Boolean, graphql_name="canUpdateServiceAccount"
    )
    """Can the current user create a `ServiceAccount` for the
    `Workspace`?
    """

    can_delete_service_account = sgqlc.types.Field(
        Boolean, graphql_name="canDeleteServiceAccount"
    )
    """Can the current user update a `ServiceAccount` in the `Workspace`?"""


########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
houston_schema.query_type = Query
houston_schema.mutation_type = Mutation
houston_schema.subscription_type = Subscription
