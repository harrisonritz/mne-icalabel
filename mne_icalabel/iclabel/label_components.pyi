from mne import BaseEpochs
from mne.io import BaseRaw
from mne.preprocessing import ICA

from .features import get_iclabel_features as get_iclabel_features
from .network import run_iclabel as run_iclabel

def iclabel_label_components(
    inst: BaseRaw | BaseEpochs,
    ica: ICA,
    inplace: bool = True,
    backend: str | None = None,
):
    """Label the provided ICA components with the ICLabel neural network.

    ICLabel is designed to classify ICs fitted with an extended infomax ICA
    decomposition algorithm on EEG datasets referenced to a common average and
    filtered between [1., 100.] Hz. It is possible to run ICLabel on datasets that
    do not meet those specification, but the classification performance
    might be negatively impacted. Moreover, the ICLabel paper did not study the
    effects of these preprocessing steps.

    ICLabel uses 3 features:

    - Topographic maps, based on the ICA decomposition.
    - Power Spectral Density (PSD), based on the ICA decomposition and the
    provided instance.
    - Autocorrelation, based on the ICA decomposition and the provided
    instance.

    For more information, see :footcite:t:`PionTonachini2019`.

    Parameters
    ----------
    inst : Raw | Epochs
    Instance used to fit the ICA decomposition. The instance should be
    referenced to a common average and bandpass filtered between 1 and
    100 Hz.
    ica : ICA
    ICA decomposition of the provided instance. The ICA decomposition
    should use the extended infomax method.
    inplace : bool
    Whether to modify the ``ica`` instance in place by adding the automatic
    annotations to the ``labels_`` property. By default True.
    backend : None | ``torch`` | ``onnx``
    Backend to use to run ICLabel. If None, returns the first available backend in
    the order ``torch``, ``onnx``.

    Returns
    -------
    labels_pred_proba : numpy.ndarray of shape (n_components, n_classes)
    The estimated corresponding predicted probabilities of output classes
    for each independent component. Columns are ordered with 'brain',
    'muscle artifact', 'eye blink', 'heart beat', 'line noise',
    'channel noise', 'other'.

    References
    ----------
    .. footbibliography::
    """
